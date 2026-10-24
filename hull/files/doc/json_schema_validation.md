# JSON schema validation within HULL

Since Helm allows to utilize JSON schema validation starting from version 3, the HULL library is strongly focused on validating as much input and output as possible.

## HULL library internal JSON schema validation

Therefore, the HULL library utilizes JSON schema validation in two places:

- Via the builtin JSON schema validation mechanism of Helm 3, the `hull` section of the merged `values.yaml` is validated against the `values.schema.json` which is included in the HULL library chart. This validates that the objects that shall be created have only valid properties defined when the charts are rendered.
- The tests included in the HULL library are executed on each release build and validate that:
  - Inputs to the test cases are validated against the `values.schema.json` which is included in the HULL chart.
  - All rendered objects are validated against the strict Kubernetes API JSON schema of the respective object types within the targeted Kubernetes version of HULL.
  The strict Kubernetes schemas used for this have been retrieved from [this project](https://github.com/instrumenta/kubernetes-json-schema) or are have been created according to [this instruction](https://github.com/instrumenta/kubernetes-json-schema/issues/26#issuecomment-747486925) when missing from the GitHub resource.

## Input JSON schema validation

Editors with a YAML language server, such as VS Code with the YAML extension or JetBrains IDEs, validate values against the schema while typing. This works for a chart's `values.yaml` directly: a file with a top-level `hull` key is validated against the HULL schema below that key, other top-level keys such as `global` or subchart values are left alone.

> Up to HULL 1.35.4, 1.36.1 and 1.37.0 the schema accepted any file with a top-level `hull` key without checking it, so editors reported no problems in such files. Helm itself was not affected because it validates the content of the `hull` key.

### Pointing a values file to the schema

The simplest way is a comment in the first line of the values file, which the YAML language server reads:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/vidispine/hull/release-1.36/hull/values.schema.json
hull:
  objects:
    deployment:
      ...
```

Use the `release-1.<minor>` branch that matches the minor version of the HULL dependency in your `Chart.yaml`. The branch always holds the schema of the latest patch release of that minor version. The GitHub release tags `hull-<version>` identify the schema of an exact version, for example `https://raw.githubusercontent.com/vidispine/hull/hull-<version>/hull/values.schema.json`.

To validate against exactly the schema of the chart's dependency, point to an unpacked copy of it with a path relative to the values file, for example `# yaml-language-server: $schema=charts/hull/values.schema.json`. `helm dependency update` stores dependencies as packages, `tar -xzf charts/hull-<version>.tgz -C charts` unpacks it.

[`hull_import.py`](/hull/files/doc/import.md) writes this comment into the `values.yaml` of the charts it creates. [`hull_validate.py`](/hull/files/doc/error_codes.md#checking-a-chart-with-hull_validatepy) performs the same validation on the command line and reports each problem on one line.

### VS Code

Instead of the comment, files can be associated with the schema in the settings:

- Install the `YAML` extension, then search the settings for "schema" and click on "Edit in settings.json".
- Associate the files to validate with the schema, given as URL or as local path:

  ```json
  "yaml.schemas": {
    "https://raw.githubusercontent.com/vidispine/hull/release-1.36/hull/values.schema.json": [ "values.yaml", "*.hull.yaml" ]
  }
  ```

---
Back to [README.md](/README.md)
