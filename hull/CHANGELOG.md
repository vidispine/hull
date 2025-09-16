# Changelog
------------------
[1.32.4]
------------------
FIXES:
- fixed error thrown due to calculation of hashsums attempted on `secret` and `configmap` object content when the object instance is implicitly disabled. Setting `enabled: false` in the corresponding `_HULL_OBJECT_TYPE_DEFAULT_` instance will implicitly disable rendering for instances which in this case don't explicitly set `enabled: true`. Now, when a `volumeMount` has property `hashsumAnnotation` set to `true` and the targeted `configmap` or `secret` is either implicitly or explicitly disabled in the chart, the calculation of the hashsum is skipped and no errors are thrown.
