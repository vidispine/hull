# Deployment

Test creation of objects and features.

* Set kind "Deployment"
* Prepare default test case for kind "Deployment" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "29" objects were rendered
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

## Short Demo - Debug true
* Prepare test case "Deployment" for kind "Deployment" and values file "values_short_demo.hull.yaml"
* Lint and Render values file "values_short_demo.hull.yaml"
* Expected number of "10" objects were rendered
* Set test object to "release-name-hull-test-myapp-frontend"
* Test Object has key "spec§template§spec§containers§0§image" with value "mycompany/myapp-frontend:v23.1"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "release-name-hull-test-myapp-backend"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "8080"
* Set test object to "release-name-hull-test-myapp-backend"
* Test Object has key "spec§template§spec§containers§0§image" with value "mycompany/myapp-backend:v23.1"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§name" with value "myappconfig"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§mountPath" with value "/etc/config/appconfig.json"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§subPath" with value "backend-appconfig.json"
* Test Object has key "spec§template§spec§volumes§0§name" with value "myappconfig"
* Test Object has key "spec§template§spec§volumes§0§configMap§name" with value "release-name-hull-test-myappconfig"
* Set test object to "release-name-hull-test-myappconfig" of kind "ConfigMap"
* Test Object has key "data§backend-appconfig.json" with value containing "\"rate-limit\": 100"
* Test Object has key "data§backend-appconfig.json" with value containing "\"max-connections\": 5"
* Test Object has key "data§backend-appconfig.json" with value containing "\"debug-log\": true"
* Set test object to "release-name-hull-test-myapp-frontend" of kind "Service"
* Test Object has key "spec§type" with value "NodePort"
* Test Object has key "spec§ports§0§nodePort" with integer value "31111"
* Test Object has key "spec§ports§0§port" with integer value "80"
* Test Object has key "spec§ports§0§targetPort" with value "http"
* Set test object to "release-name-hull-test-myapp-backend" of kind "Service"
* Test Object has key "spec§type" with value "ClusterIP"
* Test Object has key "spec§ports§0§port" with integer value "8080"
* Test Object has key "spec§ports§0§targetPort" with value "http"

## Short Demo - Debug false

* Prepare test case "Deployment" for kind "Deployment" and values file "values_short_demo.hull.yaml" including suites "debugswitch"
* Lint and Render values file "values_short_demo.hull.yaml"
* Expected number of "10" objects were rendered
* Set test object to "release-name-hull-test-myapp-frontend"
* Test Object has key "spec§template§spec§containers§0§image" with value "mycompany/myapp-frontend:v23.1"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "release-name-hull-test-myapp-backend"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "8080"
* Set test object to "release-name-hull-test-myapp-backend"
* Test Object has key "spec§template§spec§containers§0§image" with value "mycompany/myapp-backend:v23.1"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§name" with value "myappconfig"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§mountPath" with value "/etc/config/appconfig.json"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§subPath" with value "backend-appconfig.json"
* Test Object has key "spec§template§spec§volumes§0§name" with value "myappconfig"
* Test Object has key "spec§template§spec§volumes§0§configMap§name" with value "release-name-hull-test-myappconfig"
* Set test object to "release-name-hull-test-myappconfig" of kind "ConfigMap"
* Test Object has key "data§backend-appconfig.json" with value containing "\"rate-limit\": 100"
* Test Object has key "data§backend-appconfig.json" with value containing "\"max-connections\": 5"
* Test Object has key "data§backend-appconfig.json" with value not containing "\"debug-log\": true"
* Set test object to "release-name-hull-test-myapp-frontend" of kind "Service"
* Test Object has key "spec§type" with value "ClusterIP"
* Test Object has key "spec§ports§0§port" with integer value "80"
* Test Object has key "spec§ports§0§targetPort" with value "http"
* Set test object to "release-name-hull-test-myapp-backend" of kind "Service"
* Test Object has key "spec§type" with value "ClusterIP"
* Test Object has key "spec§ports§0§port" with integer value "8080"
* Test Object has key "spec§ports§0§targetPort" with value "http"
* Set test object to "release-name-hull-test-myapp" of kind "Ingress"
* Test Object has key "spec§rules§0§host" with value "SET_HOSTNAME_HERE"
* Test Object has key "spec§rules§0§http§paths§0§backend§service§name" with value "release-name-hull-test-myapp-frontend"

___

* Clean the test execution folder