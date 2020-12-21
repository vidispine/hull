# RoleBinding

Test creation of objects and features.

* Prepare default test case for kind "RoleBinding"

## Render and Validate
* Render
* Expected number of "6" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Render
* Set test object to "release-name-hull-test-no_transformation"
* Test Object has key "roleRef§name" with value "example_role"
* Test Object has key "subjects§0§name" with value "Jane"

* Set test object to "release-name-hull-test-transformation"
* Test Object has key "roleRef§name" with value "release-name-hull-test-simple"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-simple"

## Defaulting
* Render values file "values_disable_default.hull.yaml"
* Expected number of "5" objects were rendered
* Validate

## Test enable disabled and disable default
* Render values file "values_disable_default_enable_disabled.hull.yaml"
* Expected number of "6" objects were rendered
* Validate
___

* Clean the test execution folder