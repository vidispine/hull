# Changelog
------------------
[1.28.17]
------------------
FIXES:
- If HULL errors are detected during processing, the processing is not stopped immediately. Instead, all errors are collected and printed after all objects were processed, making it easier to fix multiple problems in one go.
- Multiple HULL errors in one fields value are detectable now and can be shown. Previously only one error per field value was supported.

CHANGES:
- allow combination of bool and include transformations using extended `_HT?/` prefix. Include functions in Helm can only return string values [details in this Helm issue](https://github.com/helm/helm/issues/11231) so it is not possible to set a boolean value via retrieving the result of an include function triggered by `_HT/` include. Using `_HT?/` this is possible now, when the include returns a literal `true` or `false` this is treated as a boolean value using this syntax. See the [transformation documentation](./doc/transformations.md) for a detailed explanation and examples.
- allow usage of `_HT*` get transformation path syntax within `_HT!` tpl functions and `_HT?` bool transformations to reference `values.yaml` fields. Opposed to a more implementation heavy extension of `_HT*` to add more flexibility, this solution combines full Go templating flexibility while retaining a concise way of referencing fields in the `values.yaml` via `_HT*` syntax. Additionally, in the case, where only one templating operation is required, the extended `_HT!*` prefix allows to omit the double curly brace wrapping for even more conciseness. To e.g. reference and lower case and trim a `.yaml` suffix of a `values.yaml` field, this expression may be used: `field: _HT!* _HT*hull.config.specific.source | lower | trimSuffix ".yaml"`
- due to the introduction of combined transformations with two characters after `_HT` (`_HT?/` and `_HT!*`), the syntax for `_HT**` with added serialization instructions has been changed too so that `_HT**toJson|hull.config.specific.abc` is the valid syntax now. The former legal form, `_HT*toJson|*hull.config.specific.abc`, is still usable but considered legacy from now on.
