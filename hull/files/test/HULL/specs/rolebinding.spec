# RoleBinding

Test creation of objects and features.

* Prepare default test case for kind "RoleBinding"

## Render and Validate
* Lint and Render
* Expected number of "21" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-no-transformation"
* Test Object has key "roleRef§name" with value "example_role"
* Test Object has key "subjects§0§name" with value "Jane"

* Set test object to "release-name-hull-test-transformation"
* Test Object has key "roleRef§name" with value "release-name-hull-test-simple"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-simple"
* Test Object has key "subjects§0§namespace" with value "default"

## Defaulting
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "20" objects were rendered
* Validate

## Test enable disabled and disable default
* Lint and Render values file "values_disable_default_enable_disabled.hull.yaml"
* Expected number of "20" objects were rendered
* Validate
___

* Clean the test execution folder