# Changelog
------------------
[1.29.12]
------------------
FIXES:
- fixed issue with using `_HT*` get transformation path syntax within `_HT!` tpl functions when there is an overlap in the paths of the `_HT*` expressions. Since expressions were resolved in order of appearance this could lead to unexpected results where parts of longer expressions were incorrectly overwritten. For example, having get expressions `_HT*hull.config.specific.path.api` and `_HT*hull.config.specific.path.api-user.password` could lead to `_HT*hull.config.specific.path.api` being resolved incorrectly in the latter expresison leaving `-user.password` as an invalid remainder. By sorting the found expressions by descending length instead of order of appearance, it is guaranteed that the longer paths are resolved correctly before any shorter paths that may have an overlap.
- fixed rendering error in case a Secret or ConfigMap that was referred to via the `hashsumAnnotation` feature was set to `enabled: false`. Disabled ConfigMaps or Secrets are now ignored for the calculation of hashsums.