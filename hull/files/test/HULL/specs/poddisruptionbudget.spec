# PodDisruptionBudget

Test creation of objects and features.

* Prepare default test case for kind "PodDisruptionBudget"

## Render and Validate
* Lint and Render
* Expected number of "19" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## References

* Lint and Render

* Set test object to "release-name-hull-test-simple"
* Test Object has key "spec§maxUnavailable" with integer value "1"
* Test Object has key "spec§minAvailable" with integer value "2"
* Test Object has key "spec§selector§matchLabels§name" with value "simple"