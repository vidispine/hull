# Changelog
------------------
[1.28.15]
------------------
FIXES:
- fix default RoleBinding between default Role and default ServiceAccount. Since namespace was not set for the default ServiceAccount reference, the default RBAC RoleBinding did not apply to the default ServiceAccount as intended.

CHANGES:
- add possibility to access array items in `_HT*` via using the item index for arrays instead of a dictionary key for dictionaries in the dotted path. Accessing into multiple nested arrays is possible like this `_HT*hull.config.specific.outer-list.0.inner-list.1.key`. Related feature issue is [this one](https://github.com/vidispine/hull/issues/306)
- improve debugging broken YAML errors by including all available info in the generated error message. The error message now contains the actual YAML error and the reference to the specific object type and instance which could not be rendered.
- started adding reusable helper functions for use with `_HT/` in `_util_tools.tpl`. Populating the `data` for a Secret or ConfigMap with external files matching a GLOB pattern can be achieved by using `hull.util.tools.virtualdata.data.glob`. With `hull.util.tools.file.get`, the contents of an external file can be loaded conveniently outside of the ConfigMap and Secret `data` context. Thanks [ievgenii-shepeliuk](https://github.com/ievgenii-shepeliuk) for the ideas [in this isue](https://github.com/vidispine/hull/issues/311) 