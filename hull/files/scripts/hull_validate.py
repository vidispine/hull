#!/usr/bin/env python3
"""Validate a HULL based chart and report every problem on one line.

Checks the values of a HULL based chart in two steps and stops after the first one
that finds problems:

1. JSON schema: the 'hull' values, merged like Helm does (HULL defaults, the chart's
   values.yaml, then each -f file), are validated against the values.schema.json of the
   chart's HULL dependency. Helm reports such errors as a tree of alternatives; here
   each problem becomes one line with the exact path, what is wrong, what is allowed
   and how to fix it.
2. Rendering: the chart is rendered with 'helm template' and HULL's own errors are
   reported, which already come one per line with a code and a fix.

Every problem is printed in the format of HULL's rendering errors, so that one
regular expression covers both:

  HULL failed with error [<CODE>] (@Values.<path>) <message> Fix: <hint>

Requirements: Python 3.8+, PyYAML and jsonschema. Rendering also requires helm.

Examples:
  hull_validate.py ./mychart
  hull_validate.py ./mychart -f values-prod.yaml --json
  hull_validate.py -f my.hull.yaml            # schema check of a values file only
"""

import argparse
import copy
import difflib
import json
import os
import re
import subprocess
import sys
import tarfile

import yaml

try:
    from jsonschema import Draft7Validator
except ImportError:  # pragma: no cover - reported at runtime
    Draft7Validator = None

TRANSFORMATION_PATTERN = r"^\s*(_HT[\*|\?|\^|!|&|/]|_HULL_TRANSFORMATION_<<<).*"
ERROR_LINE = "HULL failed with error [{code}] (@Values.{path}) {message}{fix}"

# How to fix each kind of schema problem. Keep in sync with hull/files/doc/error_codes.md,
# the test suite checks that every code is documented.
SCHEMA_HINTS = {
    "SCHEMA-UNKNOWN-PROPERTY": "Remove the property or move it to where it belongs. The allowed properties are listed in the message.",
    "SCHEMA-UNKNOWN-OBJECT-TYPE": "Use one of the HULL object types listed in the message, in lowercase. Kinds without an object type are created as 'generic' objects.",
    "SCHEMA-WRONG-TYPE": "Give a value of the expected type. Where a HULL transformation is allowed, a string starting with _HT is accepted too.",
    "SCHEMA-INVALID-VALUE": "Give a value that is allowed here, the message says what is expected.",
    "SCHEMA-MISSING-PROPERTY": "Add the required property.",
}

# Hints for property names that are typical mistakes when writing HULL values
PROPERTY_HINTS = {
    "spec": "HULL takes the fields of 'spec' directly below the object instance key, without 'spec:'.",
    "metadata": "Set metadata with 'labels' and 'annotations' directly below the object instance key, the name comes from the key.",
    "name": "The dictionary key is the name, remove 'name'.",
    "template": "The pod template is written as 'pod', its metadata as 'pod.labels' and 'pod.annotations'.",
    "apiVersion": "HULL sets apiVersion and kind for its object types, use a 'generic' object for other kinds.",
    "kind": "HULL sets apiVersion and kind for its object types, use a 'generic' object for other kinds.",
    "containers": "Containers belong to the pod, write them as 'pod.containers'.",
    "jobTemplate": "The job template of a CronJob is written as 'job', its pod as 'job.pod'.",
}


class Problem:

    def __init__(self, code, path, message, hint=None, phase="schema"):
        self.code, self.path, self.message, self.phase = code, path, message, phase
        self.hint = SCHEMA_HINTS.get(code) if hint is None else hint

    def line(self):
        message = self.message if re.search(r"[.!?]$", self.message) else self.message + "."
        return ERROR_LINE.format(code=self.code, path=self.path, message=message,
                                 fix=f" Fix: {self.hint}" if self.hint else "")

    def as_dict(self):
        return {"phase": self.phase, "code": self.code, "path": self.path, "message": self.message, "hint": self.hint}


# --------------------------------------------------------------------------------------
# Finding HULL and merging values like Helm
# --------------------------------------------------------------------------------------

def read_hull(path):
    """Return (values, schema, chart) of a HULL chart directory or packaged .tgz."""
    if os.path.isdir(path):
        def read(name):
            with open(os.path.join(path, name), encoding="utf-8") as file:
                return file.read()
    else:
        archive = tarfile.open(path, "r:gz")
        root = archive.getnames()[0].split("/")[0]

        def read(name):
            return archive.extractfile(f"{root}/{name}").read().decode("utf-8")
    return (yaml.safe_load(read("values.yaml")) or {}, json.loads(read("values.schema.json")),
            yaml.safe_load(read("Chart.yaml")) or {})


def find_hull(chart_dir):
    """The HULL dependency of a chart: charts/hull or charts/hull-<version>.tgz."""
    charts = os.path.join(chart_dir, "charts")
    if not os.path.isdir(charts):
        return None
    candidates = []
    for name in sorted(os.listdir(charts)):
        path = os.path.join(charts, name)
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "templates", "_objects.tpl")):
            candidates.append(path)
        elif re.match(r"^hull-\d.*\.tgz$", name):
            candidates.append(path)
    return candidates[-1] if candidates else None


def default_hull_path():
    candidate = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    return candidate if os.path.isfile(os.path.join(candidate, "templates", "_objects.tpl")) else None


def coalesce(base, override):
    """Merge override into base the way Helm merges values: maps recursively, null deletes."""
    for key, value in (override or {}).items():
        if value is None:
            base.pop(key, None)
        elif isinstance(value, dict) and isinstance(base.get(key), dict):
            coalesce(base[key], value)
        else:
            base[key] = copy.deepcopy(value)
    return base


def merged_values(hull_defaults, values_files, root_key):
    values = copy.deepcopy(hull_defaults)
    global_values = {}
    for path in values_files:
        with open(path, encoding="utf-8") as file:
            document = yaml.safe_load(file) or {}
        coalesce(values, document.get(root_key) or {})
        coalesce(global_values, document.get("global") or {})
    if global_values:
        values["global"] = global_values
    return values


# --------------------------------------------------------------------------------------
# Schema check
# --------------------------------------------------------------------------------------

def path_of(error, root_key):
    return ".".join([root_key] + [str(p) for p in error.absolute_path])


def is_transformation_branch(error):
    """The alternative that allows a HULL transformation string instead of the actual value."""
    return isinstance(error.schema, dict) and error.schema.get("pattern") == TRANSFORMATION_PATTERN


def is_placeholder_branch(error):
    """Alternatives that only exist to allow null or a transformation string."""
    return (error.validator == "type" and error.validator_value == "null") or is_transformation_branch(error)


def leaf_errors(error):
    """Descend into anyOf/oneOf alternatives and return the errors that explain the failure."""
    if not error.context:
        return [error]
    alternatives = {}
    for sub in error.context:
        alternatives.setdefault(sub.relative_schema_path[0], []).append(sub)
    transformations = any(is_transformation_branch(e) for e in error.context)
    relevant = {index: errors for index, errors in alternatives.items()
                if not all(is_placeholder_branch(e) for e in errors)}
    if not relevant:
        return [error]
    # The alternative whose errors go deepest is the one the value was meant to match,
    # all of its errors are reported. Alternatives failing at the same depth are combined,
    # like the name lists of 'propertyNames'.
    best, best_depth = [], -1
    for errors in relevant.values():
        leaves = [leaf for sub in errors for leaf in leaf_errors(sub)]
        depth = max(len(leaf.absolute_path) for leaf in leaves)
        if depth > best_depth:
            best, best_depth = leaves, depth
        elif depth == best_depth:
            best += leaves
    for leaf in best:
        if list(leaf.absolute_path) == list(error.absolute_path):
            leaf.hull_transformation_allowed = transformations
    return best


def describe(errors, root_key):
    """Turn the leaf errors of one path into one Problem."""
    error = errors[0]
    path = path_of(error, root_key)
    instance = error.instance
    property_name_errors = [e for e in errors if "propertyNames" in list(e.absolute_schema_path)]
    if property_name_errors:
        allowed = sorted({name for e in property_name_errors if e.validator == "enum" for name in e.validator_value})
        name = property_name_errors[0].instance
        message = f"Property '{name}' is not allowed here{did_you_mean(name, allowed)} Allowed are {', '.join(allowed)}"
        hint = PROPERTY_HINTS.get(str(name), SCHEMA_HINTS["SCHEMA-UNKNOWN-PROPERTY"])
        return Problem("SCHEMA-UNKNOWN-PROPERTY", path, message, hint)
    if error.validator == "additionalProperties":
        known = sorted((error.schema.get("properties") or {}).keys())
        unexpected = [k for k in instance if k not in known and not any(
            re.match(p, k) for p in (error.schema.get("patternProperties") or {}))]
        name = unexpected[0] if unexpected else ""
        if path == f"{root_key}.objects":
            return Problem("SCHEMA-UNKNOWN-OBJECT-TYPE", path, f"Object type '{name}' does not exist"
                           f"{did_you_mean(name, known)} Object types are {', '.join(known)}")
        return Problem("SCHEMA-UNKNOWN-PROPERTY", path, f"Property '{name}' is not allowed here"
                       f"{did_you_mean(name, known)} Allowed are {', '.join(known)}")
    if error.validator == "type":
        expected = sorted({t for e in errors if e.validator == "type"
                           for t in ([e.validator_value] if isinstance(e.validator_value, str) else e.validator_value)})
        expected = [t for t in expected if t != "null"] or expected
        names = {"object": "a dictionary", "array": "a list", "string": "a string", "integer": "an integer",
                 "number": "a number", "boolean": "a boolean"}
        message = f"Expected {' or '.join(names.get(t, t) for t in expected)}"
        if getattr(error, "hull_transformation_allowed", False):
            message += " or a HULL transformation"
        message += f", got {type_name(instance)} {short(instance)}"
        hint = None
        if isinstance(instance, list) and "object" in expected:
            hint = ("HULL writes named arrays like containers, env, ports or volumes as dictionaries, "
                    "the key of each element is its name.")
        return Problem("SCHEMA-WRONG-TYPE", path, message, hint)
    if error.validator == "required":
        return Problem("SCHEMA-MISSING-PROPERTY", path, error.message)
    if error.validator == "pattern":
        return Problem("SCHEMA-INVALID-VALUE", path, f"Value {short(instance)} does not match the pattern {error.validator_value}")
    if error.validator == "enum":
        return Problem("SCHEMA-INVALID-VALUE", path,
                       f"Value {short(instance)} is not one of {', '.join(map(str, error.validator_value))}")
    return Problem("SCHEMA-INVALID-VALUE", path, error.message)


def did_you_mean(name, candidates):
    """', did you mean 'x'?' for the closest candidate, '.' if there is none."""
    suggestion = difflib.get_close_matches(str(name), candidates, n=1)
    return f", did you mean '{suggestion[0]}'?" if suggestion else "."


def type_name(value):
    return {dict: "a dictionary", list: "a list", str: "the string", bool: "the boolean", int: "the integer",
            float: "the number", type(None): "null"}.get(type(value), type(value).__name__)


def short(value):
    text = json.dumps(value, default=str)
    return text if len(text) <= 60 else text[:57] + "..."


def check_schema(values, schema, root_key="hull"):
    if Draft7Validator is None:
        raise RuntimeError("the Python package 'jsonschema' is required: pip install jsonschema")
    by_path = {}
    for error in Draft7Validator(schema).iter_errors(values):
        for leaf in leaf_errors(error):
            by_path.setdefault(tuple(str(p) for p in leaf.absolute_path), []).append(leaf)
    return [describe(errors, root_key) for _, errors in sorted(by_path.items())]


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

HULL_ERROR = re.compile(r"^HULL failed with error \[([A-Z0-9-]+)\] \(@Values\.([^)]*)\) (.*?)(?: Fix: (.*))?$")


def check_rendering(chart_dir, values_files, helm, release_name, namespace):
    command = [helm, "template", release_name, chart_dir, "--namespace", namespace]
    for path in values_files:
        command += ["-f", path]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        count = sum(1 for document in yaml.safe_load_all(result.stdout) if document)
        return [], count
    problems = []
    for line in (result.stderr + result.stdout).splitlines():
        match = HULL_ERROR.match(line.strip())
        if match:
            problems.append(Problem(match.group(1), match.group(2), match.group(3), match.group(4) or "", "render"))
    if not problems:
        message = " ".join(line.strip() for line in result.stderr.splitlines() if line.strip()
                           and not line.startswith(("WARNING", "level=WARN", "Use --debug")))
        problems.append(Problem("HELM-ERROR", "", message, "", "render"))
    return problems, 0


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------

def validate(chart_dir=None, values_files=(), hull_path=None, root_key="hull", render=True, helm="helm",
             release_name="release-name", namespace="default"):
    """Validate and return (problems, summary). Used by the command line and by hull_mcp.py."""
    files = []
    if chart_dir:
        hull_path = hull_path or find_hull(chart_dir)
        if os.path.isfile(os.path.join(chart_dir, "values.yaml")):
            files.append(os.path.join(chart_dir, "values.yaml"))
    hull_path = hull_path or default_hull_path()
    if not hull_path:
        raise RuntimeError("no HULL chart found, run 'helm dependency update' for the chart or pass --hull")
    files += list(values_files)
    defaults, schema, hull_chart = read_hull(hull_path)
    problems = check_schema(merged_values(defaults, files, root_key), schema, root_key)
    summary = f"HULL {hull_chart.get('version')}: "
    if problems:
        return problems, summary + f"{len(problems)} schema problem(s)"
    if not (render and chart_dir):
        return problems, summary + "values match the schema"
    problems, count = check_rendering(chart_dir, list(values_files), helm, release_name, namespace)
    if problems:
        return problems, summary + f"values match the schema, rendering found {len(problems)} problem(s)"
    return problems, summary + f"values match the schema, {count} objects rendered without errors"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="\n\n".join(__doc__.split("\n\n")[1:]))
    parser.add_argument("chart", nargs="?", help="the chart directory, omit to check -f files against --hull only")
    parser.add_argument("-f", "--values", action="append", default=[], help="additional values file, repeatable")
    parser.add_argument("--hull", help="the HULL chart directory or .tgz (default: the chart's dependency)")
    parser.add_argument("--root-key", default="hull", help="the values key HULL is configured under (default: hull)")
    parser.add_argument("--no-render", action="store_true", help="only check the values against the schema")
    parser.add_argument("--helm", default="helm", help="helm binary used for rendering")
    parser.add_argument("--release-name", default="release-name")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--json", action="store_true", help="print the problems as JSON")
    args = parser.parse_args(argv)
    if not args.chart and not args.values:
        parser.error("give a chart directory or at least one -f values file")
    problems, summary = validate(args.chart, args.values, args.hull, args.root_key, not args.no_render, args.helm,
                                 args.release_name, args.namespace)
    if args.json:
        print(json.dumps({"summary": summary, "problems": [p.as_dict() for p in problems]}, indent=2))
    else:
        for problem in problems:
            print(problem.line())
        print(summary, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, yaml.YAMLError, tarfile.TarError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)
