# Secrets

Test creation of objects and features.

* Prepare default test case for kind "Secret"

## Render and Validate
* Lint and Render
* Expected number of "18" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Defaulting
* Lint and Render
* All test objects have key "data§default_inline_1" with Base64 encoded value of "Default Inline 1"
* All test objects have key "data§default_file_1.json" with Base64 encoded value of "\{\"name\":\"i am default_file_1.json\"\}"

* Set test object to "release-name-hull-test-defaults-no-overwrite"
* Test Object has key "data§default_inline_2" with Base64 encoded value of "Default Inline 2"
* Test Object has key "data§default_file_2.yaml" with Base64 encoded value of "name: \"i am default_file_2.yaml\""

* Set test object to "release-name-hull-test-defaults-overwrite"
* Test Object has key "data§default_inline_2" with Base64 encoded value of "Concrete Inline 2"
* Test Object has key "data§default_file_2.yaml" with Base64 encoded value of "name: \"i am concrete_file_2.yaml\""

## Templating
* Lint and Render
* Set test object to "release-name-hull-test-no-templating"
* Test Object has key "data§concrete_file_3_templated.yaml" with Base64 encoded value of "name: \"i am concrete_file_3.yaml\"\ntemplating: \"General Custom Label 1\""
* Test Object has key "data§concrete_file_3_untemplated.yaml" with Base64 encoded value of "name: \"i am concrete_file_3.yaml\"\ntemplating: \"\{\{ .Values.hull.config.general.metadata.labels.custom.general_custom_label_1 \}\}\""
* Test Object has key "data§inline_templated.txt" with Base64 encoded value of "This is an inline with a pointer to a transformation."
* Test Object has key "data§inline_untemplated.txt" with Base64 encoded value of "This is an inline with a pointer to a \{\{ .Values.hull.config.specific.resolve_me \}\}."

## Transformation
* Lint and Render
* Set test object to "release-name-hull-test-transformation-resolved"
* Test Object has key "data§concrete_file_4_resolved.txt" with Base64 encoded value of "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with Base64 encoded value of "transformation = transformation"

* Lint and Render
* Set test object to "release-name-hull-test-transformation-resolved-short"
* Test Object has key "data§concrete_file_4_resolved.txt" with Base64 encoded value of "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with Base64 encoded value of "transformation = transformation"

## Enable Data 
* Lint and Render
* Set test object to "release-name-hull-test-data-enabled-false-true"
* Test Object does not have key "data§test_disabled"
* Test Object has key "data§test_enabled" with Base64 encoded value of "This shall appear in Secret because enabled property is true"
* Test Object does not have key "data§test_disabled_transform"
* Test Object has key "data§test_enabled_transform" with Base64 encoded value of "This shall appear in Secret because enabled property is true via transformation"
* Test Object has key "data§test_enabled_missing" with Base64 encoded value of "This shall appear in Secret because enabled property is missing"

## Ordering
* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_order_test.hull.yaml"
* Lint and Render values file "values_order_test.hull.yaml"

* Test object "release-name-hull-test-aaddheaders" does not exist
* Test object "release-name-hull-test-baddheaders" does not exist
* Set test object to "release-name-hull-test-caddheaders"
* Test Object has key "data§here" with Base64 encoded value of "some data"
* Test object "release-name-hull-test-daddheaders" does not exist

## Get Transformations
* Lint and Render
* Set test object to "release-name-hull-test-test-get-variants"
* Test Object has key "data§bool_defined_true" with Base64 encoded value of "true"
* Test Object has key "data§bool_defined_false" with Base64 encoded value of "false"
* Test Object has key "data§bool_undefined" with Base64 encoded value of ""
* Test Object has key "data§string_defined" with Base64 encoded value of "i_am_string"
* Test Object has key "data§string_empty" with Base64 encoded value of ""
* Test Object has key "data§string_undefined" with Base64 encoded value of ""
* Test Object has key "data§number_defined" with Base64 encoded value of "999"
* Test Object has key "data§number_undefined" with Base64 encoded value of ""

## Include Transformation 
* Lint and Render
* Set test object to "release-name-hull-test-test-include-transformation"
* Test Object has key "data§include_name" with Base64 encoded value of "hull-test-test"
* Test Object has key "data§include_name_with_parent" with Base64 encoded value of "hull-test-test"
* Test Object has key "data§escape" with Base64 encoded value of "hull-test-split:by:colon"
* Test Object has key "data§chart_ref" with Base64 encoded value of "hull-test-1.25.0"
* Test Object has key "metadata§labels§app.kubernetes.io/component" with value "overwritten_component"
* Test Object has key "metadata§annotations§app.kubernetes.io/component" with value "overwritten_component"

## Debug options
* Fail to render the templates for values file "values_broken_get_references.hull.yaml" to test execution folder because error contains "error calling index: index of untyped nil"

* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_broken_get_references.hull.yaml" including suites "renderbrokenhullgettransformationreferences"
* Lint and Render values file "values_broken_get_references.hull.yaml"

* Set test object to "release-name-hull-test-good-reference"
* Test Object has key "metadata§labels§test" with value "trans"

* Set test object to "release-name-hull-test-broken-parent-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE --> INVALID_PATH_ELEMENT test IN hull.config.specific.test.value_to_resolve_1"

* Set test object to "release-name-hull-test-broken-leaf-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE --> INVALID_PATH_ELEMENT value_to_resolve_3 IN hull.config.specific.value_to_resolve_3"

* Prepare test case "secret" for kind "Secret" including suites "rendernilwheninlineisnil"
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with Base64 encoded value of ""
* Test Object has key "data§nothing" with Base64 encoded value of "<nil>"
* Test Object has key "data§nil" with Base64 encoded value of "<nil>"

* Prepare test case "secret" for kind "Secret" including suites "renderpathmissingwhenpathisnonexistent"
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§non_existent" with Base64 encoded value of "<path missing: files/non_existent>"

## Precedence
* Lint and Render
* Set test object to "release-name-hull-test-inline-precedence"
* Test Object has key "data§test1" with Base64 encoded value of "Inline Content"
* Test Object has key "data§test2" with Base64 encoded value of "Inline Content"

## Special cases
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with Base64 encoded value of ""
* Test Object has key "data§nothing" with Base64 encoded value of ""
* Test Object has key "data§nil" with Base64 encoded value of ""
* Test Object has key "data§non_existent" with Base64 encoded value of ""
___

* Clean the test execution folder