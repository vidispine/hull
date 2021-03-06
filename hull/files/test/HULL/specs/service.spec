# Service

Test creation of objects and features.

* Prepare default test case for kind "Service"

## Render and Validate
* Render
* Expected number of "7" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Render

* Set test object to "release-name-hull-test-loadbalancer"
* Test Object has key "spec§loadBalancerIP" with value "10.10.10.10"
* Test Object has key "spec§ports§0§port" with integer value "10"
* Test Object has key "spec§ports§0§targetPort" with integer value "1010"

* Set test object to "release-name-hull-test-nodeport"
* Test Object has key "spec§ports§0§port" with integer value "20"
* Test Object has key "spec§ports§0§targetPort" with integer value "2020"

## Selector

* Render
* Set test object to "release-name-hull-test-no_selector"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "no_selector"

* Set test object to "release-name-hull-test-selector"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "some_other_component"

___

* Clean the test execution folder