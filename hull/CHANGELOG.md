# Changelog

## [1.34.3]

CHANGES:

- support subchart usecases with HULL. First, the parsing of HULL relevant fields for transformations has been extended to all of `.Values` instead of `.Values.hull`. This means that HULL transformations in sections outside of `.Values.hull`, such as subchart configurations and `.Values.global`, are now also handled and the result is available for further processing. When adding the `hull.yaml` to a subcharts `templates/zzz` folder in a HULL based parent chart, it becomes possible to use transformations that involve shared data under `.Values.global` and make the result available to parent and sub charts.
