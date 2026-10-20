# Tools for AI agents

HULL comes with tools that let AI coding agents, and people, work with HULL charts in a closed loop: look up what is allowed, write values, check them, read a precise error, fix it. They are all part of the HULL chart, in `hull/files/scripts`, so they are available in every HULL dependency and match its version.

| Tool | Purpose |
| ---- | ------- |
| [Claude Code plugin](#claude-code-plugin) | A skill with the rules of HULL plus the MCP server below, installed in one step |
| [MCP server](#mcp-server) `hull_mcp.py` | The tools below for any agent that supports the Model Context Protocol |
| `hull_validate.py` | Checks a chart, see [checking a chart](/hull/files/doc/error_codes.md#checking-a-chart-with-hull_validatepy) |
| `hull_import.py` | Converts existing charts and manifests, see [importing charts](/hull/files/doc/import.md) |
| Schema in the editor | Validation while typing, see [JSON schema validation](/hull/files/doc/json_schema_validation.md) |

The rules themselves are summarized in the [guide for AI agents](/hull/files/doc/agents.md).

## Claude Code plugin

The HULL repository is a Claude Code plugin marketplace. Install the plugin with

```
/plugin install hull --marketplace vidispine/hull
```

or in two steps with `/plugin marketplace add vidispine/hull` and `/plugin install hull@vidispine-hull`. It provides:

- the skill `hull`, which Claude loads when it works on HULL charts: the workflow and the rules that differ from Kubernetes YAML;
- the MCP server `hull` with the tools listed below.

The plugin needs Python 3.8 or newer with PyYAML and jsonschema (`pip install pyyaml jsonschema`) and `helm`. To use the plugin of a particular HULL version, for example the one a chart depends on, unpack the chart and point Claude Code to its scripts folder: `claude --plugin-dir charts/hull/files/scripts`.

## MCP server

`hull/files/scripts/hull_mcp.py` is an MCP server with stdio transport and no dependencies besides those of the scripts. Configure it in any MCP client as the command `python3 <path to hull>/files/scripts/hull_mcp.py`, for example in Claude Code without the plugin:

```sh
claude mcp add --scope user hull -- python3 /path/to/hull/files/scripts/hull_mcp.py
```

| Tool | What it does |
| ---- | ------------ |
| `hull_docs` | Returns documentation as markdown: `guide` for the agent guide, the topics `errors`, `import`, `transformations`, `chart_design`, `schema`, `tools`, `pods`, `configmaps_secrets`, `config`, `objects`, or an error code such as `INVALID-IMAGE-DIGEST` for its explanation and fix. |
| `hull_schema` | Returns what the schema allows at a values path such as `hull.objects.deployment.web.pod.containers.main.image`, for an object type such as `deployment` or for a definition such as `hull.Container.v1`: the properties with their types and descriptions. A wrong path is answered with the closest allowed property. |
| `hull_validate` | Checks a chart like `hull_validate.py`: the values against the schema, then the rendering. Each problem is one line `HULL failed with error [CODE] (@Values.<path>) <message> Fix: <hint>`. |
| `hull_render` | Renders a chart with `helm template` and returns the objects, selected by `kind` and `name` if given, or the errors. |
| `hull_import` | Converts manifests given as text or as file into HULL values like `hull_import.py`, writes a chart if `chart_dir` is given and verifies the result. |

Each tool works with the HULL version of the chart it is used on, taken from the chart's `charts` folder. Without a chart it uses the HULL chart the server belongs to, a HULL dependency found in the project, or the latest HULL release, which it pulls with `helm`. Pulled and unpacked charts are cached in the plugin's data folder, or in `~/.cache/hull-mcp`.

---
Back to [README.md](/README.md)
