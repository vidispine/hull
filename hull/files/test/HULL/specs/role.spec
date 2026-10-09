# Role

Test creation of objects and features.

* Prepare default test case for kind "Role"

## Render and Validate
* Lint and Render
* Expected number of "2" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "rules" with array value that has "7" items

* Set test object to "release-name-hull-test-dictionary"
* Test Object has key "rules" with array value that has "3" items

## Defaulting
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render values file "values_disable_default.hull.yaml"
* Expected number of "0" objects were rendered on top of basic objects count
* Validate

## RBAC
* Prepare default test case for kind "Role"
* Lint and Render

* Test object "release-name-hull-test-default" of kind "ServiceAccount" does not exist
* Test object "release-name-hull-test-default" of kind "Role" does not exist
* Test object "release-name-hull-test-default" of kind "RoleBinding" does not exist

## RBAC with createDefaultRbacTriplet
* Prepare default test case for this kind including suites "createdefaultrbactriplet"
* Lint and Render
* Expected number of "3" objects were rendered on top of basic objects count

* Set test object to "release-name-hull-test-default" of kind "ServiceAccount"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Set test object to "release-name-hull-test-default" of kind "Role"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Set test object to "release-name-hull-test-default" of kind "RoleBinding"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"
* Test Object has key "roleRef§name" with value "release-name-hull-test-default"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-default"

* Prepare default test case for this kind including suites "createdefaultrbactriplet,norbac"
* Lint and Render

* Set test object to "release-name-hull-test-default" of kind "ServiceAccount"
* Test Object has key "metadata§name" with value "release-name-hull-test-default"

* Test object "release-name-hull-test-default" of kind "Role" does not exist
* Test object "release-name-hull-test-default" of kind "RoleBinding" does not exist

## Fail on customized default Role without createDefaultRbacTriplet
* Prepare test case "role" for kind "Role" with test chart "hull-test" and values file "values_default_rbac_triplet_guard.hull.yaml"
* Fail to render the templates for values file "values_default_rbac_triplet_guard.hull.yaml" to test execution folder because error contains "HULL failed with error (@Values.hull.objects.role.default.rules) The 'default' Role has rules but is not rendered because 'hull.config.general.createDefaultRbacTriplet' is false."

* Prepare test case "role" for kind "Role" with test chart "hull-test" and values file "values_default_rbac_triplet_guard.hull.yaml" including suites "createdefaultrbactriplet"
* Lint and Render values file "values_default_rbac_triplet_guard.hull.yaml"
* Set test object to "release-name-hull-test-default" of kind "Role"
* Test Object has key "rules" with array value that has "1" items

* Prepare test case "role" for kind "Role" with test chart "hull-test" and values file "values_default_rbac_triplet_guard_enabled.hull.yaml"
* Lint and Render values file "values_default_rbac_triplet_guard_enabled.hull.yaml"
* Set test object to "release-name-hull-test-default" of kind "Role"
* Test Object has key "rules" with array value that has "1" items
* Test object "release-name-hull-test-default" of kind "ServiceAccount" does not exist
* Test object "release-name-hull-test-default" of kind "RoleBinding" does not exist

* Prepare test case "role" for kind "Role" with test chart "hull-test" and values file "values_default_rbac_triplet_guard.hull.yaml" including suites "norbac"
* Lint the templates for values file "values_default_rbac_triplet_guard.hull.yaml" to namespace "default"
___

* Clean the test execution folder