# Changelog
------------------
[1.26.7]
------------------
CHANGES:
- introducing more flexible mechanism to populate default values for object intances. It is possible to opt to load default values from zero to multiple object instances by using new hull.base.v1 property sources. All referenced object instances are merged in the provided order to allow sharing definitions between object instances and object types. The default behavior to merge default values from _HULL_OBJECT_TYPE_DEFAULT_ remains intact.
- add icon to Chart.yaml
FIXES:
- added icon to Chart.yaml to fix linter warning
- fail with speaking error message instead of hard to decode error message when path elements in get transformations are not found