# JSON schema validation within HULL

Since Helm allows to utilize JSON schema validation starting from version 3, the HULL library is strongly focused on validating as much input and output as possible.

## HULL library internal JSON schema validation 

Therefore, the HULL library utilizes JSON schema validation in two places:

- Via the builtin JSON schema validation mechanism of Helm 3, the `hull` section of the merged `values.yaml` is validated against the `values.schema.json` which is included in the HULL library chart. This validates that the objects that shall be created have only valid properties defined when the charts are rendered.
- The tests included in the HULL library are executed on each release build and validate that:
  - Inputs to the test cases are validated against the `values.schema.json` which is included in the HULL chart.
  - All rendered objects are validated against the strict Kubernetes API JSON schema of the respective object types within the targeted Kubernetes version of HULL. 
  The strict Kubernetes schemas used for this have been retrieved from: https://github.com/instrumenta/kubernetes-json-schema or are have been created according to https://github.com/instrumenta/kubernetes-json-schema/issues/26#issuecomment-747486925 when missing from the GitHub resource.

# Input JSON schema validation
When using Editors like VSCode which support live JSON-schema validation it furthermore is possible to add input validation directly on creating the configuration with HULL. 

## VSCode

A few steps are needed to enable this feature in VSCode:

- Install the `YAML extension` in VS Code. You can install the extension directly in Visual Studio Code. Just navigate to Extensions, search for the `YAML extension` and install it.
- After installing the `YAML extension` go to settings and then search for "schema" and click on "Edit in settings.json" to configure the extension:
  - Associate the file endings you want to validate with the `values.schema.json` of HULL. 
  
  You could for example use `*.hull.yaml` as an ending for specific HULL `values.yaml` files that are merged with `values.yaml`:
  
  ```yaml
  "yaml.schemas": {
     "D:\\GIT\\hull\\hull\\values.schema.json": [ "*.hull.yaml", "values.yaml" ]
  }
  ```
  
  If you design charts with the HULL library you might want to associate `values.yaml` too so that your `values.yaml` files are validated in the IDE too.

---
Back to [README.md](./../README.md)