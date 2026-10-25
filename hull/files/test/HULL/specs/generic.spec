# Generic

Test creation of objects and features.

* Prepare default test case for kind "Generic"

## Render and Validate
* Lint and Render
* Expected number of "17" objects of kind "Dummy" were rendered
* Expected number of "1" objects of kind "Marker" were rendered
* Expected number of "1" objects of kind "Token" were rendered
* Expected number of "1" objects of kind "Policy" were rendered

## Metadata

Maybe TODO: Check basic metadata functionality

* Lint and Render

## Properties

* Lint and Render

* Set test object to "release-name-hull-test-annotated-marker" of kind "Marker"
* Test Object has key "apiVersion" with value "marker.example.com/v1"
* Test Object has key "kind" with value "Marker"

* Set test object to "release-name-hull-test-cluster-token" of kind "Token"
* Test Object has key "apiVersion" with value "v1"
* Test Object has key "kind" with value "Token"

* Set test object to "release-name-hull-test-with-fields" of kind "Policy"
* Test Object has key "apiVersion" with value "policy.example.com/v1"
* Test Object has key "spec§enforce" set to true
* Test Object has key "spec§level" with integer value "3"
* Test Object has key "rules§0§action" with value "allow"
* Test Object has key "rules§0§resource" with value "pods"
___

* Clean the test execution folder
