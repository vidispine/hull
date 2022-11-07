# Deployment

Test creation of objects and features.

* Set kind "Deployment"
* Prepare default test case for kind "Deployment" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "27" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Pod
* Lint and Render
* Check pod functionality

## Fail
* Fail to render the templates for values file "values_fail_bool.trans1.hull.yaml" to test execution folder because error contains "Does not match pattern"
* Lint and Render values file "values_fail_bool.trans2.hull.yaml"
* Fail to Validate because error contains "'true' is not of type 'boolean'"
* Fail to render the templates for values file "values_fail_integer.trans1.hull.yaml" to test execution folder because error contains "Does not match pattern"
* Fail to render the templates for values file "values_fail_integer.trans2.hull.yaml" to test execution folder because error contains "Does not match pattern"
* Lint and Render values file "values_fail_integer.trans3.hull.yaml"
* Fail to Validate because error contains "True is not of type 'integer'"
* Lint and Render values file "values_fail_integer.trans4.hull.yaml"
* Fail to Validate because error contains "'300' is not of type 'integer'"
* Lint and Render values file "values_ok_integer.trans1.hull.yaml"
* Set test object to "release-name-hull-test-ok"
* Test Object has key "spec§minReadySeconds" with integer value "300"

## Probe Port 
* Lint and Render
* Set test object to "release-name-hull-test-full-example-deployment"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§httpGet§port" with value "http"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§httpGet§port" with integer value "99"

___

* Clean the test execution folder