# Error Checking

HULL supports error checking for several cases where the rendered result would not produce valid Kubernetes YAML. The error check settings are found here in the default YAML:

```yaml
hull:
  config:
    general:
      errorChecks:
        objectYamlValid: true
        hullGetTransformationReferenceValid: true
        containerImageValid: true
        virtualFolderDataPathExists: true
        virtualFolderDataInlineValid: false
```

You can disable the implemented error checks which are by default set to `true` individually if needed even though this is not recommended. Settings which default to `false` may be enabled to enforce stricter input checking. In some cases there exists a relation to the older `hull.config.general.debug` settings which will be highlighted.

The following list is an overview of the currently implemented error checks:

- `objectYamlValid`: Basic check whether an object YAML is valid, meaning its representation is not just a dictionary containing a single `Error` key. Should always be `true` to indicate any severe problem when rendering an object.

- `hullGetTransformationReferenceValid`: Checks whether all `_HT*` references point to an existing key in the `values.yaml` object tree. If a missing element is found the error message returns the missing element and the tree path where it was expected to be found. By default set to `true` since any defined `_HT*` should originally exist in the chart.

    Note: if `hull.config.debug.renderBrokenHullGetTransformationReferences` is set to `true`, the legacy behavior where the error message is written where the reference was used but the Helm command will still be sucessful. This is not recommended, instead you should fail the Helm command hard by letting `hull.config.debug.renderBrokenHullGetTransformationReferences: false`!

- `containerImageValid`: Checks whether all containers elements (`initContainers` or `containers`) have an `image` element defined and the `image` element contains at least a `repository` sub element. A pod's container without an `image` is not valid normally so invalid `image` specs are raised as an error by default.

- `virtualFolderDataPathExists`: For `path` values in a ConfigMap or Secret it is validated that the file being referenced physically exists. Since this points to a fault in the chart design this is by default set to `true` and raised as an error.

    Note: if `hull.config.debug.renderPathMissingWhenPathIsNonExistent` is set to `true`, the legacy behavior where the missing physical file path is written to the `data` entries field will apply. This is not recommended, instead you should fail any Helm command hard by letting `hull.config.debug.renderPathMissingWhenPathIsNonExistent: false`!

- `virtualFolderDataInlineValid`: For `inline` values in a ConfigMap or Secret it is validated that the `inline` content is actually set to a value and not `null`. This can happen due to loose chart design and is not considered as an error by default but can be raised as an error by setting `virtualFolderDataInlineValid: true`.

  > Note: if `hull.config.debug.renderNilWhenInlineIsNil` is set to `true`, the legacy behavior where `<nil>` is written to the `inline` entries field if the source is not a value or `null`. This is not recommended, instead you should either leave an empty value by letting `hull.config.debug.virtualFolderDataInlineValid: false` or raise an error by `virtualFolderDataInlineValid: true`!

---
Back to [README.md](/README.md)
