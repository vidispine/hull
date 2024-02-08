# ClusterRole

Test creation of objects and features.

* Prepare default test case for kind "ClusterRole"

## Render and Validate
* Lint and Render
* Expected number of "21" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "rules" with array value that has "7" items

* Set test object to "release-name-hull-test-dictionary"
* Test Object has key "rules" with array value that has "3" items

## Defaulting
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "19" objects were rendered
* Validate
___

* Clean the test execution folder