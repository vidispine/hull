# ValidatingAdmissionPolicy

Test creation of objects and features.

* Prepare default test case for kind "ValidatingAdmissionPolicy"

## Render and Validate
* Lint and Render
* Expected number of "1" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Data

* Lint and Render

* Set test object to "release-name-hull-test-standard"
* Test Object has key "spec§failurePolicy" with value "Fail"
* Test Object has key "spec§validations§0§expression" with value "object.spec.replicas <= 5"
* Test Object has key "spec§validations§0§message" with value "too many replicas"
___

* Clean the test execution folder
