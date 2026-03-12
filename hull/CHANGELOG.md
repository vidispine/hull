# Changelog

## [1.35.2]

CHANGES:

- intoduce `conditionals` feature to allow conditional rendering of elements in places where `enabled` properties are not available. By binding one or more properties to an arbitrary condition, the rendering of the properties can be indirectly controlled which allows to render or hide sub-trees completely under specified conditions. Check the documentation on chart design for more information. Thanks Armin [sanarena](https://github.com/sanarena) for the feature request!

FIXES:

- improved error handling by storing all found HULL errors in the charts values tree instead of inline in the object YAMLs. Previously, HULL errors were written to the output YAML as the values of the properties where the errors occured and in a final parsing stage the complete YAML tree was searched and errors collected and raised. This approach was performance costly due to the complete parsing of the object YAMLs and also misses errors that happen in places which don't get rendered in the final object YAML. The new approach, that collects all errors seperately and later raises them if any are found, is less resource heavy and misses no errors.
