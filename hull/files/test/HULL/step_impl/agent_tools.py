import json
import os
import subprocess
import sys
import tempfile

import yaml
from getgauge.python import step, data_store

STEP_IMPL = os.path.dirname(os.path.realpath(__file__))
HULL_PATH = os.path.normpath(os.path.join(STEP_IMPL, '..', '..', '..', '..'))
SCRIPTS = os.path.join(HULL_PATH, 'files', 'scripts')
SOURCES = os.path.join(STEP_IMPL, '..', 'sources')


def mcp_session(calls):
    """Run the HULL MCP server, initialize it and send the calls, return the results."""
    server = subprocess.Popen([sys.executable, os.path.join(SCRIPTS, 'hull_mcp.py')], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def send(message):
        server.stdin.write(json.dumps(message) + "\n")
        server.stdin.flush()
    def receive():
        line = server.stdout.readline()
        assert line, "The MCP server closed the connection: " + server.stderr.read()
        return json.loads(line)
    try:
        send({"jsonrpc": "2.0", "id": 0, "method": "initialize",
              "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "gauge", "version": "1"}}})
        initialized = receive()
        assert initialized["result"]["protocolVersion"] == "2025-06-18", initialized
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        results = []
        for index, (method, params) in enumerate(calls, 1):
            send({"jsonrpc": "2.0", "id": index, "method": method, "params": params})
            response = receive()
            assert response["id"] == index and "result" in response, response
            results.append(response["result"])
        return results
    finally:
        server.stdin.close()
        server.wait(timeout=60)


def call_tool(name, arguments):
    result = mcp_session([("tools/call", {"name": name, "arguments": arguments})])[0]
    text = result["content"][0]["text"]
    print(text)
    assert not result["isError"], text
    return text


@step("Validate values file <file> with hull_validate.py")
def validate_values_file_with_hull_validate(file):
    result = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'hull_validate.py'), '--hull', HULL_PATH,
                             '--no-render', '-f', os.path.join(SOURCES, 'agent_tools', file)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout, result.stderr)
    data_store.scenario['validation'] = result


@step("The validation exit code is <code> and the output contains <text>")
def the_validation_exit_code_is_and_the_output_contains(code, text):
    result = data_store.scenario['validation']
    assert result.returncode == int(code), f"Exit code {result.returncode}:\n{result.stdout}\n{result.stderr}"
    assert text in result.stdout, f"'{text}' not found in:\n{result.stdout}"


@step("The HULL schema validates values below a top-level hull key")
def the_hull_schema_validates_values_below_a_top_level_hull_key():
    from jsonschema import Draft7Validator
    with open(os.path.join(HULL_PATH, 'values.schema.json'), encoding='utf-8') as file:
        validator = Draft7Validator(json.load(file))
    assert not list(validator.iter_errors({'hull': {'objects': {}}, 'global': {}, 'subchart': {'any': 1}}))
    errors = list(validator.iter_errors({'hull': {'objects': {'deploymnet': {}}}}))
    assert errors, "a values file with an unknown object type below 'hull' was accepted"
    errors = list(validator.iter_errors({'objects': {'deploymnet': {}}}))
    assert errors, "the values of the hull key itself with an unknown object type were accepted"


@step("The HULL MCP server lists the tools <names>")
def the_hull_mcp_server_lists_the_tools(names):
    result = mcp_session([("tools/list", {})])[0]
    listed = [tool["name"] for tool in result["tools"]]
    assert listed == names.split(","), listed
    for tool in result["tools"]:
        assert tool["description"] and tool["inputSchema"]["type"] == "object", tool


@step("Look up <query> with the HULL MCP schema tool and the result contains <text>")
def look_up_with_the_hull_mcp_schema_tool_and_the_result_contains(query, text):
    result = call_tool("hull_schema", {"query": query})
    assert text in result, f"'{text}' not found"


@step("Get the HULL documentation <topic> with the MCP server and the result contains <text>")
def get_the_hull_documentation_with_the_mcp_server_and_the_result_contains(topic, text):
    result = call_tool("hull_docs", {"topic": topic})
    assert text in result, f"'{text}' not found"


@step("Import manifests <file> for release <release> in namespace <namespace> into a chart with the MCP server")
def import_manifests_into_a_chart_with_the_mcp_server(file, release, namespace):
    chart_dir = os.path.join(tempfile.mkdtemp(prefix="hull-mcp-test-"), "imported")
    result = call_tool("hull_import", {"manifests_path": os.path.join(SOURCES, 'import', file), "chart_dir": chart_dir,
                                        "release_name": release, "namespace": namespace})
    assert "Verification:" in result and "different" not in result and "missing" not in result, result
    data_store.scenario['mcp_chart'] = chart_dir


@step("Validate the chart imported with the MCP server and the result contains <text>")
def validate_the_chart_imported_with_the_mcp_server_and_the_result_contains(text):
    result = call_tool("hull_validate", {"chart_dir": data_store.scenario['mcp_chart']})
    assert text in result, f"'{text}' not found"


@step("Render the chart imported with the MCP server selecting kind <kind> and the result contains <text>")
def render_the_chart_imported_with_the_mcp_server_selecting_kind_and_the_result_contains(kind, text):
    result = call_tool("hull_render", {"chart_dir": data_store.scenario['mcp_chart'], "kind": kind})
    assert text in result, f"'{text}' not found"


@step("The Claude Code plugin has the version of the HULL chart")
def the_claude_code_plugin_has_the_version_of_the_hull_chart():
    with open(os.path.join(SCRIPTS, '.claude-plugin', 'plugin.json'), encoding='utf-8') as file:
        plugin = json.load(file)
    with open(os.path.join(HULL_PATH, 'Chart.yaml'), encoding='utf-8') as file:
        chart = yaml.safe_load(file)
    assert plugin["version"] == str(chart["version"]), f"plugin.json has {plugin['version']}, Chart.yaml {chart['version']}"
    with open(os.path.join(SCRIPTS, 'skills', 'hull', 'SKILL.md'), encoding='utf-8') as file:
        skill = file.read()
    assert skill.startswith("---\nname: hull\ndescription: "), "SKILL.md frontmatter"
