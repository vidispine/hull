# Agent tools

The tools for AI agents in hull/files/scripts: hull_validate.py, the MCP server hull_mcp.py and
the Claude Code plugin around them.

## hull_validate.py reports each schema problem on one line
* Validate values file "schema-mistakes.yaml" with hull_validate.py
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-UNKNOWN-OBJECT-TYPE] (@Values.hull.objects) Object type 'deploymnet' does not exist, did you mean 'deployment'?"
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-UNKNOWN-PROPERTY] (@Values.hull.objects.deployment.named.pod.containers.main) Property 'name' is not allowed here."
* The validation exit code is "1" and the output contains "Fix: The dictionary key is the name, remove 'name'."
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-WRONG-TYPE] (@Values.hull.objects.deployment.replicas.replicas) Expected an integer or a HULL transformation, got the string \"two\"."
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-WRONG-TYPE] (@Values.hull.objects.deployment.listed.pod.containers) Expected a dictionary or a HULL transformation, got a list"
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-UNKNOWN-PROPERTY] (@Values.hull.objects.deployment.with-spec) Property 'spec' is not allowed here."
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-UNKNOWN-PROPERTY] (@Values.hull.objects.service.svc.ports.http) Property 'protocl' is not allowed here, did you mean 'protocol'?"
* The validation exit code is "1" and the output contains "HULL failed with error [SCHEMA-INVALID-VALUE] (@Values.hull.objects.deployment.named.pod.containers.main.image.digest) Value \"abc\" does not match the pattern"

## The schema validates values files with a top-level hull key
* The HULL schema validates values below a top-level hull key

## The MCP server looks up the schema and the documentation
* The HULL MCP server lists the tools "hull_docs,hull_schema,hull_validate,hull_render,hull_import"
* Look up "hull.objects.deployment.web.pod.containers.main.image" with the HULL MCP schema tool and the result contains "digest (string or transformation): The digest of the image"
* Look up "hull.objects.deployment.web.pod.containerz" with the HULL MCP schema tool and the result contains "did you mean 'containers'?"
* Look up "deployment" with the HULL MCP schema tool and the result contains "selector (object or transformation)"
* Get the HULL documentation "guide" with the MCP server and the result contains "# HULL for AI agents"
* Get the HULL documentation "SELECTOR-NOT-MATCHING-POD-LABELS" with the MCP server and the result contains "**Fix:**"

## The MCP server imports, validates and renders a chart
* Import manifests "classic-chart.yaml" for release "shop" in namespace "demo" into a chart with the MCP server
* Validate the chart imported with the MCP server and the result contains "values match the schema, 13 objects rendered without errors"
* Render the chart imported with the MCP server selecting kind "Deployment" and the result contains "# 1 of 13 rendered objects"

## The Claude Code plugin matches the chart
* The Claude Code plugin has the version of the HULL chart
