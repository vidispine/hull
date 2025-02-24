# Changelog
------------------
[1.32.2]
------------------
FIXES:
- added schema validation of Gateway API objects created in tests so they are validated properly
- corrected version of created ReferenceGrant objects from `v1` to `v1alpha2`
- fixed Gateway API incorrect schema in field `hostnames` by changing it to an array
- fixed usage of HULL transformations in all fields of Gateway API schema objects in `values.schema.json`. Additional JSON schema properties targeting regular, non-HULL transformation inputs (`pattern`, `default`, `enum`, ``minLength` and `maxLength` for strings, `format`, `minimum` and `maximum` for integers) were also applied to the `_HT` inputs which broke usage of them. Solved by strictly seperating inputs between `_HT` HULL transformation strings and regular inputs using the `anyOf` property. Thanks to [ievgenii-shepeliuk](https://github.com/ievgenii-shepeliuk) for raising the issue [here](https://github.com/vidispine/hull/issues/354)