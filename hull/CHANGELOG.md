# Changelog
------------------
[1.34.0]
------------------
FIXES:
- fixed error thrown due to calculation of hashsums attempted on `secret` and `configmap` object content when the object instance is implicitly disabled. Setting `enabled: false` in the corresponding `_HULL_OBJECT_TYPE_DEFAULT_` instance will implicitly disable rendering for instances which in this case don't explicitly set `enabled: true`. Now, when a `volumeMount` has property `hashsumAnnotation` set to `true` and the targeted `configmap` or `secret` is either implicitly or explicitly disabled in the chart, the calculation of the hashsum is skipped and no errors are thrown.

CHANGES:
- initial K8S 1.34 release
- deprecating 1.31 release
- deprecating `endpoint` object type in accordance with [Kubernetes deprecation](https://kubernetes.io/blog/2025/04/24/endpoints-deprecation/). `endpoint` remains as a configurable object type for the time being but tests for `endpoint` are removed because they fail linting starting with Kubernetes JSON schema version 1.34.