# Service

Test creation of objects and features.

* Prepare default test case for kind "Service"

## Render and Validate
* Render
* Expected number of "13" objects were rendered
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

## Enable Disable Port
* Render
* Set test object to "release-name-hull-test-port_enabled_false_true"
* Test Object has key "spec§ports" with array value that has "3" items

* Test Object has key "spec§ports§0§name" with value "test_enabled"
* Test Object has key "spec§ports§1§name" with value "test_enabled_missing"
* Test Object has key "spec§ports§2§name" with value "test_enabled_transform"

## Mixed Key Transformation
* Render
* Set test object to "release-name-hull-test-mixed_key_transformation"
* Test Object has key "spec§ports" with array value that has "4" items
* Test Object has key "spec§ports§0§name" with value "dynamic_one"
* Test Object has key "spec§ports§1§name" with value "dynamic_two"
* Test Object has key "spec§ports§2§name" with value "static_one"
* Test Object has key "spec§ports§3§name" with value "static_two"


___

* Clean the test execution folder