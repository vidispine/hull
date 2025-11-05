# Changelog
------------------
[1.33.2]
------------------
CHANGES:
- added optional parameters `NOTEMPLATING` and `SERIALIZATION` to `hull.util.tools.virtualdata.data.glob` transformation. The parameters match the behavior of `noTemplating` and `serialization` which are available for processing individual ConfigMap or Secret values. Used with the `hull.util.tools.virtualdata.data.glob` transformation, templating can be skipped and/or serialization performed on all external files captured via the given glob. Thanks [ievgenii-shepeliuk](https://github.com/ievgenii-shepeliuk) for the feature request.