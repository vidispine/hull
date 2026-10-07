# Changelog

## [1.37.1]

CHANGES:

- added the `digest` property to the container `image` specification as an alternative to `tag`, to pin images to an immutable digest. If a non-empty `digest` is set, the `image` is rendered as `<registry>/<repository>@<digest>` and the `tag` is left out. This is in line with Kubernetes, which only uses the digest for pulling when an image reference contains both, and keeps the server-side default `imagePullPolicy` at `IfNotPresent`. The `digest` format, an algorithm and a lowercase hex encoded hash joined by a colon such as `sha256:<64 hex characters>`, is validated by the JSON schema and, for values resulting from transformations, at render time by the `containerImageValid` error check. See the [image specification](/hull/files/doc/API/hull_objects_pod.md#the-hullimagev1-properties) for details.

FIXES:

- fixed the `repository` being dropped from the rendered container `image` when `hull.config.general.errorChecks.containerImageValid` is set to `false`, which resulted in invalid image references such as `:1.0`.
