# Role

Test creation of objects and features.

* Prepare default test case for kind "Role"

## Render and Validate
* Lint and Render
* Expected number of "20" objects were rendered
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
* Expected number of "17" objects were rendered
* Validate

## RBAC
* Prepare default test case for kind "Role"
* Lint and Render

* Set test object to "release-name-hull-test-default" of kind "ServiceAccount"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Set test object to "release-name-hull-test-default" of kind "Role"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Set test object to "release-name-hull-test-default" of kind "RoleBinding"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Prepare default test case for this kind including suites "norbac"
* Lint and Render

* Set test object to "release-name-hull-test-default" of kind "ServiceAccount"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Test object "release-name-hull-test-default" of kind "Role" does not exist
* Test object "release-name-hull-test-default" of kind "RoleBinding" does not exist
___

* Clean the test execution folder