# ConfigMap

Test creation of objects and features.

* Prepare default test case for kind "ConfigMap"

## Render and Validate
* Render
* Expected number of "19" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Defaulting
* Render
* All test objects have key "data§default_inline_1" with value "Default Inline 1"
* All test objects have key "data§default_file_1.json" with value "\{\"name\":\"i am default_file_1.json\"\}"

* Set test object to "release-name-hull-test-defaults_no_overwrite"
* Test Object has key "data§default_inline_2" with value "Default Inline 2"
* Test Object has key "data§default_file_2.yaml" with value "name: \"i am default_file_2.yaml\""

* Set test object to "release-name-hull-test-defaults_overwrite"
* Test Object has key "data§default_inline_2" with value "Concrete Inline 2"
* Test Object has key "data§default_file_2.yaml" with value "name: \"i am concrete_file_2.yaml\""

## Templating
* Render
* Set test object to "release-name-hull-test-no_templating"
* Test Object has key "data§concrete_file_3_templated.yaml" with value "name: \"i am concrete_file_3.yaml\"\ntemplating: \"General Custom Label 1\""
* Test Object has key "data§concrete_file_3_untemplated.yaml" with value "name: \"i am concrete_file_3.yaml\"\ntemplating: \"\{\{ .Values.hull.config.general.metadata.labels.custom.general_custom_label_1 \}\}\""
* Test Object has key "data§inline_templated.txt" with value "This is an inline with a pointer to a transformation."
* Test Object has key "data§inline_untemplated.txt" with value "This is an inline with a pointer to a \{\{ .Values.hull.config.specific.resolve_me \}\}."


## Transformation
* Render
* Set test object to "release-name-hull-test-transformation_resolved"
* Test Object has key "data§concrete_file_4_resolved.txt" with value "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with value "transformation = transformation"

* Render
* Set test object to "release-name-hull-test-transformation_resolved_short"
* Test Object has key "data§concrete_file_4_resolved.txt" with value "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with value "transformation = transformation"

## Enable Data 
* Render
* Set test object to "release-name-hull-test-data_enabled_false_true"
* Test Object does not have key "data§test_disabled"
* Test Object has key "data§test_enabled" with value "This shall appear in ConfigMap because enabled property is true"
* Test Object does not have key "data§test_disabled_transform"
* Test Object has key "data§test_enabled_transform" with value "This shall appear in ConfigMap because enabled property is true via transformation"
* Test Object has key "data§test_enabled_missing" with value "This shall appear in ConfigMap because enabled property is missing"

## Ordering
* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_order_test.hull.yaml"
* Render values file "values_order_test.hull.yaml"

* Test object "release-name-hull-test-aaddheaders" does not exist
* Test object "release-name-hull-test-baddheaders" does not exist
* Set test object to "release-name-hull-test-caddheaders"
* Test Object has key "data§here" with value "some data"
* Test object "release-name-hull-test-daddheaders" does not exist

## Get Transformations
* Render
* Set test object to "release-name-hull-test-test_get_variants"
* Test Object has key "data§bool_defined_true" with value "true"
* Test Object has key "data§bool_defined_false" with value "false"
* Test Object has key "data§bool_undefined" with value ""
* Test Object has key "data§string_defined" with value "i_am_string"
* Test Object has key "data§string_empty" with value ""
* Test Object has key "data§string_undefined" with value ""
* Test Object has key "data§number_defined" with value "999"
* Test Object has key "data§number_undefined" with value ""
* Test Object has key "data§key_with_dots_in_it" with value "hello dots!"

## Include Transformation 
* Render
* Set test object to "release-name-hull-test-test_include_transformation"
* Test Object has key "data§include_name" with value "hull-test-test"
* Test Object has key "data§include_name_with_parent" with value "hull-test-test"
* Test Object has key "data§escape" with value "hull-test-split:by:colon"
* Test Object has key "data§chart_ref" with value "hull-test-1.24.0"
* Test Object has key "metadata§labels§app.kubernetes.io/component" with value "overwritten_component"
* Test Object has key "metadata§annotations§app.kubernetes.io/component" with value "overwritten_component"

## Debug options
* Fail to render the templates for values file "values_broken_get_references.hull.yaml" to test execution folder because error contains "error calling index: index of untyped nil"

* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_broken_get_references.hull.yaml" including suites "renderbrokenhullgettransformationreferences"
* Render values file "values_broken_get_references.hull.yaml"

* Set test object to "release-name-hull-test-good_reference"
* Test Object has key "metadata§labels§test" with value "trans"

* Set test object to "release-name-hull-test-broken_parent_reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE --> INVALID_PATH_ELEMENT test IN hull.config.specific.test.value_to_resolve_1"

* Set test object to "release-name-hull-test-broken_leaf_reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE --> INVALID_PATH_ELEMENT value_to_resolve_3 IN hull.config.specific.value_to_resolve_3"

* Prepare test case "configmap" for kind "ConfigMap" including suites "rendernilwheninlineisnil"
* Render
* Set test object to "release-name-hull-test-special_cases"
* Test Object has key "data§empty" with value ""
* Test Object has key "data§nothing" with value "<nil>"
* Test Object has key "data§nil" with value "<nil>"

* Prepare test case "configmap" for kind "ConfigMap" including suites "renderpathmissingwhenpathisnonexistent"
* Render
* Set test object to "release-name-hull-test-special_cases"
* Test Object has key "data§non_existent" with value "<path missing: files/non_existent>"

## Precedence
* Render
* Set test object to "release-name-hull-test-inline_precedence"
* Test Object has key "data§test1" with value "Inline Content"
* Test Object has key "data§test2" with value "Inline Content"

## Special cases
* Render
* Set test object to "release-name-hull-test-special_cases"
* Test Object has key "data§empty" with value ""
* Test Object has key "data§nothing" with value ""
* Test Object has key "data§nil" with value ""
* Test Object has key "data§non_existent" with value ""

## Binary Data
* Render
* Set test object to "release-name-hull-test-binary_data_hull"
* Test Object has key "binaryData§binary_from_file" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

* Set test object to "release-name-hull-test-binary_data"
* Test Object has key "binaryData§binary" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

* Set test object to "release-name-hull-test-binary_data_mixed"
* Test Object has key "binaryData§binary" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"
* Test Object has key "binaryData§binary_from_file" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

___

* Clean the test execution folder