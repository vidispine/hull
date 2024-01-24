# Changelog
------------------
[1.27.10]
------------------
CHANGES:
- removed hardcoded `type: Opaque` and allow to freely set type of Secrets, thanks [khmarochos](https://github.com/khmarochos) for [PR](https://github.com/vidispine/hull/pull/275)
- enabled specification of `configmap` and `secret` `data` inline` fields as dictionaries or lists and added implicit and explicit serialization to `configmap` and `secret` `data` entries. Implicit and automatic serialization takes place for files ending with `.json` (`toPrettyJson`) and files ending with `.yaml` and `.yml` (`toYaml`) if the `inline` content is a dictionary or a list. Explicit serialization is possible using the new `serialization` property for `data` elements and can be applied to dictionary, list and string `inline` entries and string `path` contents. Thanks [khmarochos](https://github.com/khmarochos) for the idea [in this report](https://github.com/vidispine/hull/issues/267)
- added optional serialization arguments to `_HT/` and `_HT*` to serialize dictioanry and lists `toJson`, `toPrettyJson`, `toRawJson`, `toString` or `toYaml`, also thanks [khmarochos](https://github.com/khmarochos) for the idea [in this report](https://github.com/vidispine/hull/issues/267)
- added optional `postRender` option to inject object instance key or object name strings into rendered object YAML. This enables very efficient specification of multiple identical object instances via the `sources` and `_HULL_OBJECT_TYPE_DEFAULT_` feature and last-minute insertion of the actual object instance key or name into the rendered YAML string. Handle with caution since this can invalidate the YAML structure!
- added error checks in HULL to prevent common configuration errors by failing the Helm command. By default verify `image` specifications exist and are valid for all `containers`, files pointed to via `path` physically exist and all tree elements in a `_HT*` references are resolvable

FIXES:
- fixed hashsumAnnotation calculation of secrets incorrectly being done on Base64 encoded value instead of decoded value
- centralized `configmap` and `secret` functionality and tests to guarantee exact same handling whether content is defined `inline` or in a file with `path`. Code difference between `secret` and `configmap` reduced to only late base64 value encoding in the case of secrets.
- improved code in helper functions, thanks [JuryA](https://github.com/JuryA) for [PR](https://github.com/vidispine/hull/pull/277)
