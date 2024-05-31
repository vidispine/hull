# Changelog
------------------
[1.30.2]
------------------
CHANGES:
- allow to force render an otherwise disabled object using `hull.object.base.xyz` include by setting FORCE_ENABLED to true. This opens up the possibility to define object instance templates in HULL which are not deployed by HULL itself (by setting `enabled: false`). Instead, the object template can be rendered to a ConfigMap as a full-fledged Kubernetes YAML object which for example can serve as an object template the underlying application creates instances from.