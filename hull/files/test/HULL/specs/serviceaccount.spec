# ServiceAccount

Test creation of objects and features.

* Prepare default test case for kind "ServiceAccount"

## Render and Validate
* Lint and Render
* Expected number of "1" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "automountServiceAccountToken" set to true
* Test Object has key "imagePullSecrets" with array value that has "1" items

## Defaulting
* Prepare default test case for this kind including suites "defaultrbacobjects"
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "0" objects were rendered on top of basic objects count
* Validate

## Opt in to default RBAC objects
* Prepare default test case for this kind including suites "defaultrbacobjects"
* Lint and Render
* Expected number of "2" objects were rendered on top of basic objects count
* Set test object to "release-name-hull-test-default"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"
* Validate
___

* Clean the test execution folder