# RoleBinding

Test creation of objects and features.

* Prepare default test case for kind "RoleBinding"

## Render and Validate
* Lint and Render
* Expected number of "2" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-no-transformation"
* Test Object has key "roleRef§name" with value "example_role"
* Test Object has key "subjects§0§name" with value "Jane"

* Set test object to "release-name-hull-test-transformation"
* Test Object has key "roleRef§name" with value "release-name-hull-test-simple"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-simple"
* Test Object has key "subjects§0§namespace" with value "default"

## Defaulting
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "2" objects were rendered on top of basic objects count
* Validate

## Test enable disabled and disable default
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render values file "values_disable_default_enable_disabled.hull.yaml"
* Expected number of "2" objects were rendered on top of basic objects count
* Validate

## Opt in with createDefaultRbacTriplet
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render
* Expected number of "3" objects were rendered on top of basic objects count
* Set test object to "release-name-hull-test-default"
* Test Object has key "roleRef§name" with value "release-name-hull-test-default"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-default"
* Test Object has key "subjects§0§kind" with value "ServiceAccount"
* Validate

## Fail on customized default RoleBinding without createDefaultRbacTriplet
* Prepare test case "rolebinding" for kind "RoleBinding" with test chart "hull-test" and values file "values_default_rbac_triplet_guard.hull.yaml"
* Fail to render the templates for values file "values_default_rbac_triplet_guard.hull.yaml" to test execution folder because error contains "HULL failed with error (@Values.hull.objects.rolebinding.default.subjects) The 'default' RoleBinding has a customized roleRef or subjects but is not rendered because 'hull.config.general.createDefaultRbacTriplet' is false."
___

* Clean the test execution folder