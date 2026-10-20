import os
import re
from getgauge.python import step

HULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', '..')


@step("Every HULL error code has a fix hint and is documented")
def every_hull_error_code_has_a_fix_hint_and_is_documented():
    templates = os.path.join(HULL_PATH, 'templates')
    raised = set()
    for name in os.listdir(templates):
        if name.endswith('.tpl'):
            with open(os.path.join(templates, name), encoding='utf-8') as file:
                raised |= set(re.findall(r'"ERROR_TYPE" "([A-Z0-9-]+)"', file.read()))
    assert raised, "No error codes found in " + templates

    with open(os.path.join(templates, '_util.tpl'), encoding='utf-8') as file:
        hints = re.search(r'define "hull\.util\.error\.hints" -}}\n(.*?)\n{{- end -}}', file.read(), re.S)
    assert hints, "Template hull.util.error.hints not found"
    hinted = set(re.findall(r'^([A-Z0-9-]+):', hints.group(1), re.M))

    # the schema problems reported by hull_validate.py have their hints in the script
    with open(os.path.join(HULL_PATH, 'files', 'scripts', 'hull_validate.py'), encoding='utf-8') as file:
        validator = file.read()
    schema_hints = re.search(r'^SCHEMA_HINTS = {\n(.*?)\n}', validator, re.S | re.M)
    assert schema_hints, "SCHEMA_HINTS not found in hull_validate.py"
    schema_codes = set(re.findall(r'^    "([A-Z0-9-]+)": ', schema_hints.group(1), re.M))
    raised |= schema_codes
    hinted |= schema_codes

    with open(os.path.join(HULL_PATH, 'files', 'doc', 'error_codes.md'), encoding='utf-8') as file:
        documented = set(re.findall(r'^### `([A-Z0-9-]+)`\s*$', file.read(), re.M))

    problems = []
    for code in sorted(raised - hinted):
        problems.append(f"{code} is raised but has no hint in hull.util.error.hints")
    for code in sorted(raised - documented):
        problems.append(f"{code} is raised but has no '### `{code}`' section in error_codes.md")
    for code in sorted((hinted | documented) - raised):
        problems.append(f"{code} has a hint or documentation but is never raised")
    assert not problems, "\n".join(problems)
