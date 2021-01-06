# Ingress

Test creation of objects and features.

* Prepare default test case for kind "Ingress"

## Render and Validate
* Render
* Expected number of "5" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Static Naming
* Render
* Set test object to "release-name-hull-test-staticnames"
* Test Object has key "spec§rules§0§http§paths§0§path" with value "/external"
* Test Object has key "spec§rules§0§http§paths§0§backend§service§name" with value "external_service"
* Test Object has key "spec§rules§1§http§paths§0§path" with value "/standard"
* Test Object has key "spec§rules§1§http§paths§0§backend§service§name" with value "release-name-hull-test-service1_standard"
* Test Object has key "spec§rules§2§http§paths§0§path" with value "/transform"
* Test Object has key "spec§rules§2§http§paths§0§backend§service§name" with value "release-name-hull-test-full_name_transformed"
* Test Object has key "spec§tls§0§secretName" with value "external_secret"
* Test Object has key "spec§tls§1§secretName" with value "release-name-hull-test-local_secret"

___

* Clean the test execution folder