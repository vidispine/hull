#!/usr/bin/env python3
"""MCP server for writing, checking and converting HULL based Helm charts.

A Model Context Protocol server (stdio transport) with tools for AI agents:

  hull_docs      the HULL guide for agents, error codes and other documentation
  hull_schema    the properties allowed at a values path, for an object type or a definition
  hull_validate  check a chart: schema problems and rendering errors, one line each
  hull_render    render a chart with helm template, optionally only some objects
  hull_import    convert Kubernetes manifests into HULL values, optionally verified

Every tool uses the HULL version the chart at hand depends on: the dependency in the
chart's charts/ folder, otherwise a HULL chart found in the project, the HULL chart this
script is part of, or finally the latest release pulled with helm.

Requirements: Python 3.8+ and PyYAML; jsonschema for the schema check of hull_validate;
helm for rendering, verifying and pulling HULL.

Claude Code: install the 'hull' plugin of this repository, see hull/files/doc/agent_tools.md.
Other MCP clients: run 'python3 <path>/hull_mcp.py' as a stdio server.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import traceback
import urllib.request

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import hull_import  # noqa: E402
import hull_validate  # noqa: E402

HULL_REPOSITORY = "https://vidispine.github.io/hull"
SERVER_NAME = "hull"
INSTRUCTIONS = ("Tools for Helm charts built with the HULL library, whose Kubernetes objects are values under "
                "hull.objects instead of templates. Read hull_docs (topic 'guide') before writing HULL values, "
                "run hull_validate after every change and fix what it reports, use hull_schema to look up allowed "
                "properties and hull_import to convert existing manifests or charts.")


# --------------------------------------------------------------------------------------
# Finding the HULL chart to use
# --------------------------------------------------------------------------------------

def cache_dir():
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(os.path.expanduser("~"), ".cache", "hull-mcp")
    os.makedirs(base, exist_ok=True)
    return base


def unpacked(path):
    """A HULL chart directory for a directory or a packaged chart."""
    if os.path.isdir(path):
        return path
    with open(path, "rb") as file:
        digest = hashlib.sha256(file.read()).hexdigest()[:16]
    target = os.path.join(cache_dir(), f"unpacked-{digest}")
    if not os.path.isdir(os.path.join(target, "hull")):
        with tarfile.open(path, "r:gz") as archive:
            members = [m for m in archive.getmembers() if not os.path.isabs(m.name) and ".." not in m.name.split("/")]
            archive.extractall(target, members=members)
    return os.path.join(target, "hull")


def project_hull():
    """The newest HULL dependency found in the charts of the project."""
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    found = []
    for directory, subdirectories, _ in os.walk(root):
        depth = directory[len(root):].count(os.sep)
        subdirectories[:] = [d for d in subdirectories if not d.startswith(".") and d != "node_modules"]
        if depth > 5:
            subdirectories[:] = []
            continue
        if os.path.basename(directory) == "charts":
            candidate = hull_validate.find_hull(os.path.dirname(directory))
            if candidate:
                found.append(candidate)
    def version(path):
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", os.path.basename(path)) if path.endswith(".tgz") else None
        if not match and os.path.isdir(path):
            with open(os.path.join(path, "Chart.yaml"), encoding="utf-8") as file:
                match = re.search(r"(\d+)\.(\d+)\.(\d+)", str(yaml.safe_load(file).get("version")))
        return tuple(int(x) for x in match.groups()) if match else (0, 0, 0)
    return max(found, key=version) if found else None


def version_key(version):
    return tuple(int(x) for x in version.split("."))


_newest_release = []


def newest_release():
    """The newest HULL version in the chart repository, looked up once per server start; None if offline."""
    if not _newest_release:
        version = None
        try:
            with urllib.request.urlopen(f"{HULL_REPOSITORY}/index.yaml", timeout=30) as response:
                entries = ((yaml.safe_load(response.read()) or {}).get("entries") or {}).get("hull") or []
            versions = [str(e.get("version")) for e in entries if re.match(r"^\d+\.\d+\.\d+$", str(e.get("version")))]
            version = max(versions, key=version_key) if versions else None
        except (OSError, ValueError, yaml.YAMLError):
            pass
        _newest_release.append(version)
    return _newest_release[0]


def pulled_hull(version=None):
    """A HULL release pulled with helm, cached by version. Without a version the newest release, or the
    newest cached one if the chart repository cannot be reached."""
    version = version or newest_release()
    if not version:
        cached = [d[len("pulled-"):] for d in os.listdir(cache_dir()) if re.match(r"^pulled-\d+\.\d+\.\d+$", d)
                  and os.path.isfile(os.path.join(cache_dir(), d, "hull", "Chart.yaml"))]
        if cached:
            return os.path.join(cache_dir(), f"pulled-{max(cached, key=version_key)}", "hull")
        raise RuntimeError(f"no HULL chart found locally and {HULL_REPOSITORY} cannot be reached")
    target = os.path.join(cache_dir(), f"pulled-{version}")
    if not os.path.isfile(os.path.join(target, "hull", "Chart.yaml")):
        shutil.rmtree(target, ignore_errors=True)
        command = ["helm", "pull", "hull", "--repo", HULL_REPOSITORY, "--version", version, "--untar", "--untardir", target]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        if result.returncode != 0:
            raise RuntimeError(f"no HULL chart found locally and pulling it failed: {result.stderr.strip()}")
    return os.path.join(target, "hull")


def resolve_hull(chart_dir=None, hull=None):
    if hull:
        return unpacked(hull)
    if chart_dir:
        dependency = hull_validate.find_hull(chart_dir)
        if dependency:
            return unpacked(dependency)
    own = hull_validate.default_hull_path()
    if own:
        return own
    found = project_hull()
    return unpacked(found) if found else pulled_hull()


def chart_version(hull_dir):
    with open(os.path.join(hull_dir, "Chart.yaml"), encoding="utf-8") as file:
        return str(yaml.safe_load(file).get("version"))


# --------------------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------------------

DOC_TOPICS = {
    "guide": "agents.md", "cookbook": "cookbook.md", "errors": "error_codes.md", "import": "import.md",
    "transformations": "transformations.md",
    "chart_design": "chart_design.md", "schema": "json_schema_validation.md", "tools": "agent_tools.md",
    "pods": "API/hull_objects_pod.md", "configmaps_secrets": "API/hull_objects_configmaps_secrets.md",
    "config": "API/hull_config.md", "objects": "API/hull_objects_.md",
}


def doc_file(hull_dir, name):
    """A documentation file of the HULL chart, or of the newest release if the chart predates the file.
    Returns the path, the HULL version it belongs to and a note if that is not the chart's version."""
    path = os.path.join(hull_dir, "files", "doc", name)
    if os.path.isfile(path):
        return path, chart_version(hull_dir), ""
    try:
        newest = pulled_hull()
    except RuntimeError:
        return None, None, ""
    path = os.path.join(newest, "files", "doc", name)
    if not os.path.isfile(path):
        return None, None, ""
    return path, chart_version(newest), (f"Note: HULL {chart_version(hull_dir)}, which is used here, has no {name}. "
                                         f"This is the documentation of HULL {chart_version(newest)}, its HISTORY.md "
                                         f"lists what was added since {chart_version(hull_dir)}.\n\n")


def tool_docs(topic="guide", chart_dir=None):
    hull_dir = resolve_hull(chart_dir)
    if re.match(r"^[A-Z0-9]+(-[A-Z0-9]+)+$", topic or ""):
        path, _, note = doc_file(hull_dir, "error_codes.md")
        if not path:
            raise ValueError(f"HULL {chart_version(hull_dir)} has no error code documentation, error codes were "
                             f"added in 1.35.5, 1.36.2 and 1.37.1")
        with open(path, encoding="utf-8") as file:
            text = file.read()
        match = re.search(rf"^### `{re.escape(topic)}`\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
        if not match:
            raise ValueError(f"unknown error code {topic}")
        return note + f"### `{topic}`\n{match.group(1)}".strip()
    if topic not in DOC_TOPICS:
        raise ValueError(f"unknown topic '{topic}', use one of {', '.join(DOC_TOPICS)} or an error code")
    path, version, note = doc_file(hull_dir, DOC_TOPICS[topic])
    if not path:
        raise ValueError(f"HULL {chart_version(hull_dir)} has no '{topic}' documentation, it was added in a later "
                         f"version. See https://github.com/vidispine/hull/tree/main/hull/files/doc")
    with open(path, encoding="utf-8") as file:
        return note + f"(HULL {version})\n\n" + file.read()


def tool_validate(chart_dir=None, values_files=(), render=True, release_name="release-name", namespace="default"):
    if not chart_dir and not values_files:
        raise ValueError("give chart_dir or values_files")
    problems, summary = hull_validate.validate(chart_dir, list(values_files),
                                               None if chart_dir else resolve_hull(),
                                               render=render, release_name=release_name, namespace=namespace)
    return "\n".join([summary] + [p.line() for p in problems])


def tool_render(chart_dir, values_files=(), release_name="release-name", namespace="default", kube_version=None,
                kind=None, name=None, max_chars=60000):
    command = ["helm", "template", release_name, chart_dir, "--namespace", namespace]
    for path in values_files:
        command += ["-f", path]
    if kube_version:
        command += ["--kube-version", kube_version]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        lines = [line for line in result.stderr.splitlines() if line.startswith("HULL failed with error")]
        return "Rendering failed:\n" + ("\n".join(lines) if lines else result.stderr.strip())
    documents = [d for d in yaml.safe_load_all(result.stdout) if d]
    selected = [d for d in documents
                if (not kind or str(d.get("kind", "")).lower() == kind.lower())
                and (not name or name in str((d.get("metadata") or {}).get("name", "")))]
    text = "---\n".join(hull_import.dump(d) for d in selected)
    header = f"# {len(selected)} of {len(documents)} rendered objects\n"
    if len(text) > max_chars:
        text = text[:max_chars] + "\n# ... truncated, use 'kind' or 'name' to select fewer objects\n"
    return header + text


def tool_import(manifests=None, manifests_path=None, chart_dir=None, chart_name=None, release_name="release-name",
                namespace="default", verify=True, hull=None):
    if bool(manifests) == bool(manifests_path):
        raise ValueError("give either manifests (YAML text) or manifests_path")
    objects = (hull_import.parse_documents(manifests, "<manifests>") if manifests
               else hull_import.load_objects([manifests_path]))
    hull_dir = resolve_hull(hull=hull) if hull else resolve_hull()
    converter = hull_import.Converter(namespace=namespace, features=hull_import.hull_features(hull_dir))
    values = converter.convert(objects)
    values_text = hull_import.schema_modeline(hull_dir) + hull_import.dump(values)
    output = []
    results = None
    if chart_dir or verify:
        target = chart_dir or tempfile.mkdtemp(prefix="hull-import-")
        name = chart_name or os.path.basename(os.path.abspath(target)).lower()
        if not re.match(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", name):
            name = "imported"
        hull_import.write_chart(target, name, values_text, hull_dir)
        try:
            if verify:
                rendered = hull_import.render("helm", target, release_name, namespace, None)
                results = hull_import.verify(objects, rendered, converter.generated_port_names)
        finally:
            if not chart_dir:
                shutil.rmtree(target, ignore_errors=True)
        if chart_dir:
            output.append(f"Wrote the HULL {chart_version(hull_dir)} based chart to {chart_dir}.")
    for note in converter.notes:
        output.append(f"[{note.level}] {note.ref}: {note.message}")
    if results is not None:
        counts = {}
        for result in results:
            counts[result["status"]] = counts.get(result["status"], 0) + 1
            if result["status"] != "identical":
                output.append(f"[{result['status']}] {result['object']}")
                for difference in result["differences"]:
                    output.append(f"    {difference['path']}: {json.dumps(difference['original'])} -> "
                                  f"{json.dumps(difference['rendered'])}")
        output.append("Verification: " + ", ".join(f"{c} {s}" for s, c in sorted(counts.items())))
    if not chart_dir:
        output.append("Values:\n" + values_text)
    return "\n".join(output)


# ---- schema lookup --------------------------------------------------------------------

def resolve_ref(schema, node, seen=None):
    seen = seen or set()
    while isinstance(node, dict) and "$ref" in node and node["$ref"].startswith("#/definitions/"):
        name = node["$ref"].split("/", 2)[2]
        if name in seen:
            break
        seen.add(name)
        node = schema["definitions"][name]
    return node


def branches(schema, node):
    """The node and all schemas it combines, references resolved."""
    node = resolve_ref(schema, node)
    result, stack, seen = [], [node], set()
    while stack:
        current = resolve_ref(schema, stack.pop())
        if not isinstance(current, dict) or id(current) in seen:
            continue
        seen.add(id(current))
        result.append(current)
        for key in ("allOf", "anyOf", "oneOf"):
            stack += current.get(key, [])
        for key in ("then", "else"):
            if key in current:
                stack.append(current[key])
    return result


def children(schema, node):
    properties, patterns, names = {}, [], set()
    for branch in branches(schema, node):
        for key, value in (branch.get("properties") or {}).items():
            properties.setdefault(key, value)
        patterns += list((branch.get("patternProperties") or {}).items())
        property_names = branch.get("propertyNames")
        if property_names:
            for alternative in branches(schema, property_names):
                names |= set(alternative.get("enum") or [])
    return properties, patterns, names


def describe_type(schema, node):
    types, transformation = set(), False
    for branch in branches(schema, node):
        if branch.get("pattern") == hull_validate.TRANSFORMATION_PATTERN:
            transformation = True
            continue
        value = branch.get("type")
        if isinstance(value, str):
            types.add(value)
        elif isinstance(value, list):
            types |= set(value)
    result = "/".join(sorted(types - {"null"})) or ("string" if transformation else "any")
    return result + (" or transformation" if transformation and types - {"null"} else "")


def first_sentence(text):
    text = (text or "").strip().replace("\n", " ")
    match = re.match(r"(.+?\.)(\s|$)", text)
    return (match.group(1) if match else text)[:220]


def tool_schema(query, chart_dir=None):
    hull_dir = resolve_hull(chart_dir)
    with open(os.path.join(hull_dir, "values.schema.json"), encoding="utf-8") as file:
        schema = json.load(file)
    definitions = schema["definitions"]
    objects = definitions["root"]["properties"]["objects"]["properties"]
    if query in definitions:
        node, title = definitions[query], f"definition {query}"
    elif query in objects:
        node, title = objects[query]["patternProperties"]["^[^_].*$"], f"object type {query}"
    else:
        path = query.split(".")
        if path and path[0] == "hull":
            path = path[1:]
        node, walked = definitions["root"], ["hull"]
        for segment in path:
            properties, patterns, _ = children(schema, node)
            if segment in properties:
                node = properties[segment]
            else:
                matching = [value for pattern, value in patterns if re.match(pattern, segment)]
                if not matching:
                    known = sorted(properties)
                    return (f"No property '{segment}' below {'.'.join(walked)}"
                            f"{hull_validate.did_you_mean(segment, known)} Allowed are {', '.join(known)}")
                node = matching[0]
            walked.append(segment)
        title = f"values path {'.'.join(walked)}"
    properties, patterns, names = children(schema, node)
    resolved = resolve_ref(schema, node)
    lines = [f"HULL {chart_version(hull_dir)} schema for {title}: {describe_type(schema, node)}"]
    description = resolved.get("description") if isinstance(resolved, dict) else None
    if description:
        lines.append(first_sentence(description))
    if properties:
        lines.append("Properties:")
        for key in sorted(properties):
            value = properties[key]
            description = value.get("description") or (resolve_ref(schema, value) or {}).get("description")
            lines.append(f"  {key} ({describe_type(schema, value)}): {first_sentence(description)}")
    extra = sorted(names - set(properties))
    if extra:
        lines.append("Also allowed: " + ", ".join(extra))
    for pattern, value in patterns:
        if pattern == "^[^_].*$":
            lines.append(f"Any key not starting with '_': {describe_type(schema, value)}, "
                         f"look up '<path>.<key>' for its properties")
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# MCP protocol
# --------------------------------------------------------------------------------------

STRING_LIST = {"type": "array", "items": {"type": "string"}}
TOOLS = [
    {
        "name": "hull_docs",
        "description": "Returns HULL documentation as markdown. Read topic 'guide' before writing HULL values: it has "
                       "the rules that differ from Kubernetes YAML, the workflow and the transformations. Topic "
                       "'cookbook' has tested recipes for common tasks. Pass an error code such as "
                       "'SELECTOR-NOT-MATCHING-POD-LABELS' to get its explanation and fix.",
        "inputSchema": {"type": "object", "properties": {
            "topic": {"type": "string", "description": "guide, cookbook, errors, import, transformations, chart_design, "
                                                       "schema, tools, pods, configmaps_secrets, config, objects, or an "
                                                       "error code"},
            "chart_dir": {"type": "string", "description": "a chart, to use the docs of its HULL version"}}},
        "function": tool_docs,
    },
    {
        "name": "hull_schema",
        "description": "Looks up what the HULL schema allows: give a values path such as "
                       "'hull.objects.deployment.web.pod.containers.main' (any key works for instance and element "
                       "names), an object type such as 'deployment', or a definition name such as 'hull.Container.v1'. "
                       "Returns the properties with types and descriptions.",
        "inputSchema": {"type": "object", "required": ["query"], "properties": {
            "query": {"type": "string"},
            "chart_dir": {"type": "string", "description": "a chart, to use the schema of its HULL version"}}},
        "function": tool_schema,
    },
    {
        "name": "hull_validate",
        "description": "Checks a HULL based chart: first the values against the schema, then the rendering. Reports "
                       "every problem on one line as 'HULL failed with error [CODE] (@Values.path) message Fix: hint'. "
                       "Run it after every change of the values and fix all problems.",
        "inputSchema": {"type": "object", "properties": {
            "chart_dir": {"type": "string", "description": "the chart directory, its HULL dependency must be in charts/"},
            "values_files": dict(STRING_LIST, description="additional values files, like helm -f"),
            "render": {"type": "boolean", "description": "also render the chart (default true)"},
            "release_name": {"type": "string"}, "namespace": {"type": "string"}}},
        "function": tool_validate,
    },
    {
        "name": "hull_render",
        "description": "Renders a chart with helm template and returns the objects as YAML, or the errors. Use "
                       "'kind' and 'name' (substring) to return only some objects.",
        "inputSchema": {"type": "object", "required": ["chart_dir"], "properties": {
            "chart_dir": {"type": "string"}, "values_files": STRING_LIST, "release_name": {"type": "string"},
            "namespace": {"type": "string"}, "kube_version": {"type": "string"}, "kind": {"type": "string"},
            "name": {"type": "string"}}},
        "function": tool_render,
    },
    {
        "name": "hull_import",
        "description": "Converts Kubernetes manifests, for example the output of helm template of an existing chart, "
                       "into HULL values and verifies that they render the same objects. With chart_dir a complete "
                       "HULL based chart is written there. Returns the notes, the verification result and, without "
                       "chart_dir, the values.",
        "inputSchema": {"type": "object", "properties": {
            "manifests": {"type": "string", "description": "the manifests as YAML text"},
            "manifests_path": {"type": "string", "description": "a YAML file or directory with the manifests"},
            "chart_dir": {"type": "string", "description": "directory to write the new chart to"},
            "chart_name": {"type": "string"},
            "release_name": {"type": "string", "description": "the release name the manifests were rendered for"},
            "namespace": {"type": "string", "description": "the namespace the manifests were rendered for"},
            "verify": {"type": "boolean", "description": "render and compare with the input (default true)"},
            "hull": {"type": "string", "description": "HULL chart directory or .tgz to use"}}},
        "function": tool_import,
    },
]


def handle(message):
    method = message.get("method")
    if "id" not in message:
        return None  # notifications, e.g. notifications/initialized
    if method == "initialize":
        requested = (message.get("params") or {}).get("protocolVersion")
        # the tools used here exist in all protocol versions, so the client's version is accepted
        version = requested if isinstance(requested, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", requested) else "2025-06-18"
        hull_dir = hull_validate.default_hull_path()
        return {"protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": chart_version(hull_dir) if hull_dir else "plugin"},
                "instructions": INSTRUCTIONS}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{k: v for k, v in tool.items() if k != "function"} for tool in TOOLS]}
    if method == "tools/call":
        params = message.get("params") or {}
        tool = next((t for t in TOOLS if t["name"] == params.get("name")), None)
        if not tool:
            raise JsonRpcError(-32602, f"unknown tool {params.get('name')}")
        arguments = params.get("arguments") or {}
        allowed = set(tool["inputSchema"]["properties"])
        unknown = set(arguments) - allowed
        if unknown:
            return {"content": [{"type": "text", "text": f"unknown arguments {', '.join(sorted(unknown))}, "
                                                          f"allowed are {', '.join(sorted(allowed))}"}],
                    "isError": True}
        try:
            text = tool["function"](**arguments)
            return {"content": [{"type": "text", "text": text}], "isError": False}
        except Exception as error:  # reported to the agent instead of failing the protocol
            detail = traceback.format_exc(limit=3) if os.environ.get("HULL_MCP_DEBUG") else ""
            return {"content": [{"type": "text", "text": f"{type(error).__name__}: {error}\n{detail}".strip()}],
                    "isError": True}
    raise JsonRpcError(-32601, f"method not found: {method}")


class JsonRpcError(Exception):

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def serve(stdin=sys.stdin, stdout=sys.stdout):
    while True:
        line = stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as error:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"parse error: {error}"}}
        else:
            try:
                result = handle(message)
                if result is None:
                    continue
                response = {"jsonrpc": "2.0", "id": message["id"], "result": result}
            except JsonRpcError as error:
                response = {"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": error.code, "message": str(error)}}
        stdout.write(json.dumps(response) + "\n")
        stdout.flush()


if __name__ == "__main__":
    serve()
