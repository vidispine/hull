# ConfigMap

Test creation of objects and features.

* Prepare default test case for kind "ConfigMap"

## Render and Validate
* Render
* Expected number of "16" objects were rendered
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