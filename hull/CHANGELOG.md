# Changelog
------------------
[1.29.13]
------------------
FIXES:
- fixed follow-up problem with a previous fix for calculation of `hashsumAnnotation` for ConfigMaps or Secrets. In an unlikely case, where a ConfigMap or Secret object has no `data` property set and is then disabled, an unintended error was thrown. ConfigMaps or Secrets with no actual `data` properties can now be disabled without the `hashsumAnnotation` functionality failing. 

CHANGES:
- added include shortform transformation `_HT/` to the allowed transformations that can be used within `_HT!` tpl transformations. Similar to using the `_HT*` get syntax within `_HT!` transformations, the `_HT/` include syntax is now embeddable as well. To delimit the `_HT/` arguments from the rest of the `_HT!` content, the `_HT/` block must have a clear ending suffix `/TH_`, similar to bashs `if`/`fi` style. For example, the following syntax now executes the include function within the tpl content: `_HT!{{- printf "%s-%s" _HT/hull.metadata.name:COMPONENT:"tpl-include"/TH_ "example" -}}`
- added possibility to override individual object instance namespaces by setting an optional `namespaceOverride` property on the object instance. CAUTION: creating objects in multiple namespaces _may_ go against Helm principles since normally all objects are created only in the release namespace!  
- added more example `values.yaml` files to `files/examples` and updated outdated ones