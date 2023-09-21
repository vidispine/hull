# Service

Test creation of objects and features.

* Prepare default test case for kind "Service"

## Render and Validate
* Lint and Render
* Expected number of "24" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render

* Set test object to "release-name-hull-test-loadbalancer"
* Test Object has key "spec§loadBalancerIP" with value "10.10.10.10"
* Test Object has key "spec§ports§0§port" with integer value "10"
* Test Object has key "spec§ports§0§targetPort" with integer value "1010"

* Set test object to "release-name-hull-test-nodeport"
* Test Object has key "spec§ports§0§port" with integer value "20"
* Test Object has key "spec§ports§0§targetPort" with integer value "2020"

## Selector

* Lint and Render
* Set test object to "release-name-hull-test-no-selector"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "no-selector"

* Set test object to "release-name-hull-test-selector"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "some_other_component"

## Enable Disable Port
* Lint and Render
* Set test object to "release-name-hull-test-port-enabled-false-true"
* Test Object has key "spec§ports" with array value that has "3" items

* Test Object has key "spec§ports§0§name" with value "test_enabled"
* Test Object has key "spec§ports§1§name" with value "test_enabled_missing"
* Test Object has key "spec§ports§2§name" with value "test_enabled_transform"

## Mixed Key Transformation
* Lint and Render
* Set test object to "release-name-hull-test-mixed-key-transformation"
* Test Object has key "spec§ports" with array value that has "4" items
* Test Object has key "spec§ports§0§name" with value "dynamic_one"
* Test Object has key "spec§ports§1§name" with value "dynamic_two"
* Test Object has key "spec§ports§2§name" with value "static_one"
* Test Object has key "spec§ports§3§name" with value "static_two"

## Full Transformation
* Lint and Render
* Set test object to "release-name-hull-test-full-transformation"
* Test Object has key "spec§ports" with array value that has "2" items
* Test Object has key "spec§ports§0§name" with value "dynamic_one"
* Test Object has key "spec§ports§1§name" with value "dynamic_two"
___

* Clean the test execution folder