# Changelog
------------------
[1.29.1]
------------------
CHANGES:
- removed all required field definitions from values.schema.json. Required fields are helpful on the output side because they indicate which fields are important in the rendered output but on input side side they block the full potential of efficient defaulting. When present, The JSON schema demands that they are added to all individual instances of an object - even when a source or _HULL_OBJECT_TYPE_DEFAULT_ has already set them appropriately and concisely. This leads to unnecessary bloat and complexity in the values.yaml and therefore the usage of required fields in the JSON schema was dropped favor of cleaner chart design.
- added tests to solidify expectations on workarounds for YAML parser issues with large numbers (unwanted rendering in scientific notation, unwanted interpretation of strings as scientific notation). The issues mentioned [in this report](https://github.com/vidispine/hull/issues/262) cannot be solved in HULL but the ests should from now on indicate if something has changed in Helm about the applicability of the workarounds, thanks [seniorquico](https://github.com/seniorquico)

FIXES:
- fixed bug where imagePullSecrets cannot be overwritten with empty list, thanks [khmarochos](https://github.com/khmarochos)