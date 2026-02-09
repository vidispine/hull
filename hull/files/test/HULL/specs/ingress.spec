# Ingress

Test creation of objects and features.

* Prepare default test case for kind "Ingress"

## Render and Validate
* Lint and Render
* Expected number of "10" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Static Naming
* Lint and Render
* Set test object to "release-name-hull-test-staticnames"
* Test Object has key "spec§rules§0§http§paths§0§path" with value "/external"
* Test Object has key "spec§rules§0§http§paths§0§backend§service§name" with value "external_service"
* Test Object has key "spec§rules§1§http§paths§0§path" with value "/standard"
* Test Object has key "spec§rules§1§http§paths§0§backend§service§name" with value "release-name-hull-test-service1_standard"
* Test Object has key "spec§rules§2§http§paths§0§path" with value "/transform"
* Test Object has key "spec§rules§2§http§paths§0§backend§service§name" with value "release-name-hull-test-full_name_transformed"
* Test Object has key "spec§tls§0§secretName" with value "external_secret"
* Test Object has key "spec§tls§1§secretName" with value "release-name-hull-test-local_secret"

## Enable Disable Tls Rules 
* Lint and Render
* Set test object to "release-name-hull-test-tls-rules-enabled-false-true"
* Test Object has key "spec§tls" with array value that has "3" items
* Test Object has key "spec§rules" with array value that has "3" items

* Test Object has key "spec§rules§0§host" with value "test_enabled.two.com"
* Test Object has key "spec§rules§1§host" with value "test_enabled_missing.two.com"
* Test Object has key "spec§rules§2§host" with value "test_enabled_transform.two.com"

* Test Object has key "spec§tls§0§secretName" with value "release-name-hull-test-test_enabled"
* Test Object has key "spec§tls§1§secretName" with value "release-name-hull-test-test_enabled_missing"
* Test Object has key "spec§tls§2§secretName" with value "release-name-hull-test-test_enabled_transform"

* Test Object has key "spec§rules§0§http§paths" with array value that has "3" items
* Test Object has key "spec§rules§0§http§paths§0§path" with value "/test_enabled"
* Test Object has key "spec§rules§0§http§paths§1§path" with value "/test_enabled_missing"
* Test Object has key "spec§rules§0§http§paths§2§path" with value "/test_enabled_transform"

## Test sources feature
* Lint and Render
* Set test object to "release-name-hull-test-stream"
* Test Object has key "metadata§annotations§ingress.kubernetes.io/rewrite-target" with value "/dash"

## External templates
* Prepare default test case for this kind with test chart "hull-test" and values file "values" including suites "" and chartmods "externaltemplates"
* Lint and Render values file "values_external_templates.hull.yaml"

* Set test object to "referencegrants.gateway.networking.k8s.io" of kind "CustomResourceDefinition"
* Test Object has key "spec§versions§0§schema§openAPIV3Schema§properties§apiVersion§default" with value "1.2.3.4.5"

## Subchart shared global variables
* Prepare default test case for this kind with test chart "hull-test" and values file "values_subcharts" including suites "" and chartmods "subcharts"
* Lint and Render values file "values_subcharts.hull.yaml"

* Set test object to "release-name-hull-test-test-global"
* Test Object has key "spec§rules§0§http§paths§0§backend§service§port§number" with integer value "111"

* Set test object to "release-name-kube-state-metrics" of kind "Service"
* Test Object has key "spec§ports§0§port" with integer value "333"
* Test Object has key "spec§type" with value "NodePort"
* Test Object has key "metadata§annotations§annotation_1" with value "Global Annotation 1"
* Test Object has key "metadata§annotations§annotation_2" with value "Global Annotation 2"
* Test Object has key "spec§clusterIP" with value "123.345.431.543"
* Test Object has key "spec§ipFamilies§0" with value "IPv6"
* Test Object has key "spec§ipFamilies§1" with value "IPv4"
* Test Object has key "spec§ipFamilyPolicy" with value "PreferDualStack"

* Set test object to "release-name-prometheus-postgres-exporter" of kind "Service"
* Test Object has key "spec§ports§0§port" with integer value "333"
* Test Object has key "spec§type" with value "LoadBalancer"
* Test Object has key "metadata§annotations§annotation_1" with value "Global Annotation 1"
* Test Object has key "metadata§annotations§annotation_2" with value "Global Annotation 2"
* Test Object has key "metadata§annotations§annotation_3" with value "Local Annotation 1"
* Test Object has key "metadata§annotations§annotation_4" with value "Local Annotation 2"
* Test Object has key "spec§ports§0§targetPort" with integer value "333"


___

* Clean the test execution folder