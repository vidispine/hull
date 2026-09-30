# ServiceAccount

Test creation of objects and features.

* Prepare default test case for kind "ServiceAccount"

## Render and Validate
* Lint and Render
* Expected number of "1" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "automountServiceAccountToken" set to true
* Test Object has key "imagePullSecrets" with array value that has "1" items

## Defaulting
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "0" objects were rendered on top of basic objects count
* Validate

## Opt in with createDefaultRbacTriplet
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render
* Expected number of "2" objects were rendered on top of basic objects count
* Set test object to "release-name-hull-test-default"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"
* Validate

## Fail on customized default ServiceAccount without createDefaultRbacTriplet
* Prepare test case "serviceaccount" for kind "ServiceAccount" with test chart "hull-test" and values file "values_default_rbac_triplet_guard.hull.yaml"
* Fail to render the templates for values file "values_default_rbac_triplet_guard.hull.yaml" to test execution folder because error contains "HULL failed with error (@Values.hull.objects.serviceaccount.default.annotations) The 'default' ServiceAccount has annotations but is not rendered because 'hull.config.general.createDefaultRbacTriplet' is false."

* Prepare test case "serviceaccount" for kind "ServiceAccount" with test chart "hull-test" and values file "values_default_rbac_triplet_guard_disabled.hull.yaml"
* Lint and Render values file "values_default_rbac_triplet_guard_disabled.hull.yaml"
* Test object "release-name-hull-test-default" of kind "ServiceAccount" does not exist
___

* Clean the test execution folder