# Job

Test creation of objects and features.

* Prepare default test case for kind "Job" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "27" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Pod
* Lint and Render
* Check pod functionality

## Selector
* Lint and Render
* Set test object to "release-name-hull-test-no-selector-provided"
* Test Object does not have key "spec§selector"

* Set test object to "release-name-hull-test-selector-provided"
* Test Object has key "spec§selector§matchLabels§test_label" with value "test_value"

___


* Clean the test execution folder