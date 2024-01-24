# ResourceQuota

Test creation of objects and features.

* Prepare default test case for kind "ResourceQuota"

## Render and Validate
* Lint and Render
* Expected number of "19" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Data

* Lint and Render

* Set test object to "release-name-hull-test-quota-one"
* Test Object has key "spec§hard§cpu" with value "10"
* Test Object has key "spec§hard§memory" with value "20Gi"
* Test Object has key "spec§scopes§0" with value "scope_one"
* Test Object has key "spec§scopes§1" with value "scope_two"
___

* Clean the test execution folder