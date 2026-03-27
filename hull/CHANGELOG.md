# Changelog

## [1.34.4]

CHANGES:

- introduce `conditionals` feature to allow conditional rendering of elements in places where `enabled` properties are not available. By binding one or more properties to an arbitrary condition, the rendering of the properties can be indirectly controlled which allows to render or hide sub-trees completely under specified conditions. Check the documentation on chart design for more information. Thanks Armin [sanarena](https://github.com/sanarena) for the feature request!

FIXES:

- fixed error handling changes because it caused installation failures with [errors in disabled content](https://github.com/vidispine/hull/issues/401) and [sub chart rendering](https://github.com/vidispine/hull/issues/393). Instead of the changed approach (raising every error that occurs during processing) and the original approach (raise only errors in rendered objects), a combined approach is used now. The old error handling practice is restored (raise all visible errors in templates) but extended with raising errors from `conditionals` references, however this is limited to the cases where the associated object is actually rendered. If errors in `conditional` references are recorded for objects that don't get rendered in the end, the errors are dropped.
- improved error messages for better understanding and added object tree paths for direct identification of error source
- improved error handling by storing all found HULL errors in the charts values tree instead of inline in the object YAMLs. Previously, HULL errors were written to the output YAML as the values of the properties where the errors occured and in a final parsing stage the complete YAML tree was searched and errors collected and raised. This approach was performance costly due to the complete parsing of the object YAMLs and also misses errors that happen in places which don't get rendered in the final object YAML. The new approach, that collects all errors separately and later raises them if any are found, is less resource heavy and misses no errors.
