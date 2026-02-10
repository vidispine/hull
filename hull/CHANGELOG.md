# Changelog

## [1.33.4]

CHANGES:

- support subchart usecases with HULL. First, the parsing of HULL relevant fields for transformations has been extended to all of `.Values` instead of `.Values.hull`. This means that HULL transformations in sections outside of `.Values.hull`, such as subchart configurations and `.Values.global`, are now also handled and the result is available for further processing. When adding the `hull.yaml` to a subcharts `templates/zzz` folder in a HULL based parent chart, it becomes possible to use transformations that involve shared data under `.Values.global` and make the result available to parent and sub charts.

FIXES:

- due to [changes made to Helm 3 versions](https://github.com/helm/helm/issues/30587), the behavior for accessing undefined values has changed for specific Helm 3 versions starting with 3.19.5+ and 3.20+. The named versions (and potentially all following Helm 3 patches) exhibit the Helm 4 behavior which leads to an error if an undefined field is accessed. Tests were adapted to differentiate concrete Helm 3 versions and set correct expectations.
