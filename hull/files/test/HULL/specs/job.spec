# Job

Test creation of objects and features.

* Prepare default test case for kind "Job" including suites "pod"

## Render and Validate
* Render
* Expected number of "17" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Pod
* Render
* Check pod functionality

## Selector
* Render
* Set test object to "release-name-hull-test-no_selector_provided"
* Test Object does not have key "spec§selector"

* Set test object to "release-name-hull-test-selector_provided"
* Test Object has key "spec§selector§matchLabels§test_label" with value "test_value"

___


* Clean the test execution folder