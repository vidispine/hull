# ServiceAccount

Test creation of objects and features.

* Prepare default test case for kind "ServiceAccount"

## Render and Validate
* Lint and Render
* Expected number of "20" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "automountServiceAccountToken" set to true
* Test Object has key "imagePullSecrets" with array value that has "1" items

## Defaulting
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "18" objects were rendered
* Validate
___

* Clean the test execution folder