# Deployment

Test creation of objects and features.

* Set kind "Deployment"
* Prepare default test case for kind "Deployment" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "40" objects were rendered
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
* Expected number of "19" objects were rendered
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
* Expected number of "19" objects were rendered
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

## Sources Example
* Prepare test case "Deployment" for kind "Deployment" and values file "values_sources_example.hull.yaml"
* Lint and Render values file "values_sources_example.hull.yaml"
* Expected number of "23" objects were rendered

* Set test object to "release-name-hull-test-app-python-direct"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-python-direct:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_CONNECTIONSTRING"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "jdbc:sqlserver://a.b.com:9988;databaseName=database-a-b-c;user=user-abc;password=pass-abc;"
* Test Object has key "spec§template§spec§containers§0§env§1§name" with value "DATABASE_HOST"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "a.b.com"
* Test Object has key "spec§template§spec§containers§0§env§2§name" with value "DATABASE_NAME"
* Test Object has key "spec§template§spec§containers§0§env§2§value" with value "database-a-b-c"
* Test Object has key "spec§template§spec§containers§0§env§3§name" with value "DATABASE_PASSWORD"
* Test Object has key "spec§template§spec§containers§0§env§3§value" with value "pass-abc"
* Test Object has key "spec§template§spec§containers§0§env§4§name" with value "DATABASE_PORT"
* Test Object has key "spec§template§spec§containers§0§env§4§value" with value "9988"
* Test Object has key "spec§template§spec§containers§0§env§5§name" with value "DATABASE_USERNAME"
* Test Object has key "spec§template§spec§containers§0§env§5§value" with value "user-abc"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§httpGet§path" with value "/_health"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§httpGet§port" with value "http"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§initialDelaySeconds" with integer value "60"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§failureThreshold" with integer value "20"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§successThreshold" with integer value "1"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§periodSeconds" with integer value "30"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§timeoutSeconds" with integer value "20"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§httpGet§path" with value "/_health"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§httpGet§port" with value "http"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§initialDelaySeconds" with integer value "30"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§failureThreshold" with integer value "4"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§successThreshold" with integer value "1"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§periodSeconds" with integer value "15"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§timeoutSeconds" with integer value "20"

* Set test object to "release-name-hull-test-app-java-direct"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-java-direct:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_CONNECTIONSTRING"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "jdbc:sqlserver://a.b.com:9988;databaseName=database-a-b-c;user=user-abc;password=pass-abc;"
* Test Object has key "spec§template§spec§containers§0§env§1§name" with value "DATABASE_HOST"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "a.b.com"
* Test Object has key "spec§template§spec§containers§0§env§2§name" with value "DATABASE_NAME"
* Test Object has key "spec§template§spec§containers§0§env§2§value" with value "database-a-b-c"
* Test Object has key "spec§template§spec§containers§0§env§3§name" with value "DATABASE_PASSWORD"
* Test Object has key "spec§template§spec§containers§0§env§3§value" with value "pass-abc"
* Test Object has key "spec§template§spec§containers§0§env§4§name" with value "DATABASE_PORT"
* Test Object has key "spec§template§spec§containers§0§env§4§value" with value "9988"
* Test Object has key "spec§template§spec§containers§0§env§5§name" with value "DATABASE_USERNAME"
* Test Object has key "spec§template§spec§containers§0§env§5§value" with value "user-abc"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§httpGet§path" with value "/_health"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§httpGet§port" with value "http"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§initialDelaySeconds" with integer value "60"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§failureThreshold" with integer value "20"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§successThreshold" with integer value "1"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§periodSeconds" with integer value "30"
* Test Object has key "spec§template§spec§containers§0§livenessProbe§timeoutSeconds" with integer value "20"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§httpGet§path" with value "/_health"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§httpGet§port" with value "http"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§initialDelaySeconds" with integer value "30"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§failureThreshold" with integer value "4"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§successThreshold" with integer value "1"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§periodSeconds" with integer value "15"
* Test Object has key "spec§template§spec§containers§0§readinessProbe§timeoutSeconds" with integer value "20"

* Set test object to "release-name-hull-test-app-python-1"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-python-1:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env" with array value that has "5" items
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_HOST"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "a.b.com"
* Test Object has key "spec§template§spec§containers§0§env§1§name" with value "DATABASE_NAME"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "database-a-b-c"
* Test Object has key "spec§template§spec§containers§0§env§2§name" with value "DATABASE_PASSWORD"
* Test Object has key "spec§template§spec§containers§0§env§2§value" with value "pass-abc"
* Test Object has key "spec§template§spec§containers§0§env§3§name" with value "DATABASE_PORT"
* Test Object has key "spec§template§spec§containers§0§env§3§value" with value "9988"
* Test Object has key "spec§template§spec§containers§0§env§4§name" with value "DATABASE_USERNAME"
* Test Object has key "spec§template§spec§containers§0§env§4§value" with value "user-abc"
* Test Object does not have key "spec§template§spec§containers§0§livenessProbe"
* Test Object does not have key "spec§template§spec§containers§0§readinessProbe"
* Test Object has key "spec§template§spec§containers§1§image" with value "myrepo/app-python-sec-1:23.3.2"
* Test Object has key "spec§template§spec§containers§1§env" with array value that has "6" items
* Test Object has key "spec§template§spec§containers§1§env§0§name" with value "DATABASE_HOST"
* Test Object has key "spec§template§spec§containers§1§env§0§value" with value "a.b.com"
* Test Object has key "spec§template§spec§containers§1§env§1§name" with value "DATABASE_NAME"
* Test Object has key "spec§template§spec§containers§1§env§1§value" with value "database-a-b-c"
* Test Object has key "spec§template§spec§containers§1§env§2§name" with value "DATABASE_PASSWORD"
* Test Object has key "spec§template§spec§containers§1§env§2§value" with value "pass-abc"
* Test Object has key "spec§template§spec§containers§1§env§3§name" with value "DATABASE_PORT"
* Test Object has key "spec§template§spec§containers§1§env§3§value" with value "9988"
* Test Object has key "spec§template§spec§containers§1§env§4§name" with value "DATABASE_USERNAME"
* Test Object has key "spec§template§spec§containers§1§env§4§value" with value "user-abc"
* Test Object has key "spec§template§spec§containers§1§env§5§name" with value "FROM_DEFAULT"
* Test Object has key "spec§template§spec§containers§1§env§5§value" with value "target value"

* Set test object to "release-name-hull-test-app-python-2"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-python-2:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env" with array value that has "5" items
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_HOST"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "a.b.com"
* Test Object has key "spec§template§spec§containers§0§env§1§name" with value "DATABASE_NAME"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "database-a-b-c"
* Test Object has key "spec§template§spec§containers§0§env§2§name" with value "DATABASE_PASSWORD"
* Test Object has key "spec§template§spec§containers§0§env§2§value" with value "pass-abc"
* Test Object has key "spec§template§spec§containers§0§env§3§name" with value "DATABASE_PORT"
* Test Object has key "spec§template§spec§containers§0§env§3§value" with value "9988"
* Test Object has key "spec§template§spec§containers§0§env§4§name" with value "DATABASE_USERNAME"
* Test Object has key "spec§template§spec§containers§0§env§4§value" with value "user-abc"
* Test Object does not have key "spec§template§spec§containers§0§livenessProbe"
* Test Object does not have key "spec§template§spec§containers§0§readinessProbe"

* Set test object to "release-name-hull-test-app-java-1"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-java-1:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env" with array value that has "1" items
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_CONNECTIONSTRING"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "jdbc:sqlserver://a.b.com:9988;databaseName=database-a-b-c;user=user-abc;password=pass-abc;"
* Test Object does not have key "spec§template§spec§containers§0§livenessProbe"
* Test Object does not have key "spec§template§spec§containers§0§readinessProbe"

* Set test object to "release-name-hull-test-app-java-2"
* Test Object has key "spec§template§spec§containers§0§image" with value "myrepo/app-java-2:23.3.2"
* Test Object has key "spec§template§spec§containers§0§env" with array value that has "2" items
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "DATABASE_CONNECTIONSTRING"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "jdbc:sqlserver://a.b.com:9988;databaseName=database-a-b-c;user=user-abc;password=pass-abc;"
* Test Object has key "spec§template§spec§containers§0§env§1§name" with value "LOADED_FROM_JOB"
* Test Object has key "spec§template§spec§containers§0§env§1§value" with value "external___loaded"
* Test Object does not have key "spec§template§spec§containers§0§livenessProbe"
* Test Object does not have key "spec§template§spec§containers§0§readinessProbe"
___

* Clean the test execution folder