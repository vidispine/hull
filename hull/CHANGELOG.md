# Changelog

## [1.37.1]

CHANGES:

- added the `digest` property to the container `image` specification as an alternative to `tag`, to pin images to an immutable digest. If a non-empty `digest` is set, the `image` is rendered as `<registry>/<repository>@<digest>` and the `tag` is left out. This is in line with Kubernetes, which only uses the digest for pulling when an image reference contains both, and keeps the server-side default `imagePullPolicy` at `IfNotPresent`. The `digest` format, an algorithm and a lowercase hex encoded hash joined by a colon such as `sha256:<64 hex characters>`, is validated by the JSON schema and, for values resulting from transformations, at render time by the `containerImageValid` error check. See the [image specification](/hull/files/doc/API/hull_objects_pod.md#the-hullimagev1-properties) for details.
- added error codes and fix hints to all HULL rendering errors. Each error is reported on one line of the form `HULL failed with error [<CODE>] (@Values.<path>) <message> Fix: <hint>`, followed by a pointer to the new [error codes](/hull/files/doc/error_codes.md) documentation that explains every code with its causes and fixes. The codes are stable, so scripts and AI agents can rely on them. Messages may now contain any characters including colons and show the offending value where it helps, image errors point to the exact values path including `pod`, identical errors of an object are reported once, and the errors for missing `sources` that previously stopped rendering with a plain message use the same format.
- added the optional `selector` property to `deployment`, `statefulset` and `daemonset` objects, `job` objects already accepted it. If set, HULL renders it instead of the generated selector and does not add its generated selector labels to the pod template. This allows to take over objects of existing releases whose selectors cannot be changed.
- added the `SELECTOR-NOT-MATCHING-POD-LABELS` check: rendering fails if the `selector.matchLabels` of an object are not all present in its pod template labels. Kubernetes rejects such objects, so far they were rendered anyway, for example when object `labels` override one of the generated selector labels.
- added `hull/files/scripts/hull_import.py`, which converts Kubernetes manifests, for example the `helm template` output of an existing chart, into HULL values, optionally writes a complete HULL based chart and verifies that the chart renders the same objects. See [importing charts](/hull/files/doc/import.md).
- added the [guide for AI agents](/hull/files/doc/agents.md), which states the rules of HULL, the workflow, the transformations and how Kubernetes kinds map to HULL object types on one page, and an `llms.txt` index of the documentation.

FIXES:

- fixed the `repository` being dropped from the rendered container `image` when `hull.config.general.errorChecks.containerImageValid` is set to `false`, which resulted in invalid image references such as `:1.0`.
- fixed the JSON schema of `generic` objects, which rejected every property besides `apiVersion`, `kind` and the object base properties, contrary to the documentation. Any property is now accepted and rendered as given.
- fixed errors in `conditionals` being raised in HULL's internal marker format instead of a readable message.
- fixed the message of the error for an object whose rendered YAML cannot be parsed, its parts were in the wrong order.
