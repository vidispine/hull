# JSON schema validation within HULL

Since Helm allows to utilize JSON schema validation starting from version 3, the HULL library is strongly focused on validating as much as possible.

## Internal JSON schema validation 

The HULL library utilizes JSON schema validation in two places:

- The `hull` section of the merged `values.yaml` is validated against the `values.schema.json` which is included in the HULL chart. This verifies that the objects that should be created have only valid properties defined when the charts are rendered.
- The tests included in the HULL library are executed on each build and validate that:
  - Inputs to the tests are validated against against the `values.schema.json` which is included in the HULL chart.
  - All rendered objects are validated against the strict K8S JSON schema of the respective object within the targeted Kubernetes version of HULL. 
  The K8S schemas used have been retrieved from: https://github.com/instrumenta/kubernetes-json-schema

# Input JSON schema validation
When using VSCode it furthermore is possible to add input validation directly on creating the configuration with HULL. A few steps are needed to enable this feature:

- Install the `YAML extension` in VS Code. You can install the extension directly in Visual Studio Code. Just navigate to Extensions, search for the `YAML extension` and install it.
- After installing the `YAML extension` go to settings and then search for "schema" and click on "Edit in settings.json" to configure the extension:
  - Associate the file endings you want to validate with the `values.schema.json` of HULL:
  
  
  ```yaml
  "yaml.schemas": {
     "D:\\GIT\\hull\\hull\\values.schema.json": "*.hull.yaml"
  }