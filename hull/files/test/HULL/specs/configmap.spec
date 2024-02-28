# ConfigMap

Test creation of objects and features.

* Prepare default test case for kind "ConfigMap"
* Prepare default test case for this kind including suites "virtualfolderdata,globalmetadata,objecttypemetadata"

## Render and Validate
* Lint and Render
* Expected number of "36" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Defaulting
* Lint and Render
* All test objects have key "data§default_inline_1" with value "Default Inline 1"
* All test objects have key "data§default_file_1.json" with value of key "default_file_1.json" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-defaults-no-overwrite"
* Test Object has key "data§default_inline_2" with value "Default Inline 2"
* Test Object has key "data§default_file_2.yaml" with value "name: i am default_file_2.yaml"

* Set test object to "release-name-hull-test-defaults-overwrite"
* Test Object has key "data§default_inline_2" with value "Concrete Inline 2"
* Test Object has key "data§default_file_2.yaml" with value "name: i am concrete_file_2.yaml"

## Templating
* Lint and Render
* Set test object to "release-name-hull-test-no-templating"
* Test Object has key "data§concrete_file_3_templated.yaml" with value "name: i am concrete_file_3.yaml\ntemplating: General Custom Label 1"
* Test Object has key "data§concrete_file_3_untemplated.yaml" with value of key "concrete_file_3_untemplated.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline_templated.txt" with value "This is an inline with a pointer to a transformation."
* Test Object has key "data§inline_untemplated.txt" with value "This is an inline with a pointer to a \{\{ .Values.hull.config.specific.resolve_me \}\}."

## Transformation
* Lint and Render
* Set test object to "release-name-hull-test-transformation-resolved"
* Test Object has key "data§concrete_file_4_resolved.txt" with value "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with value "transformation = transformation"
* Set test object to "release-name-hull-test-transformation-resolved-short"
* Test Object has key "data§concrete_file_4_resolved.txt" with value "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with value "transformation = transformation"

## Enable Data 
* Lint and Render
* Set test object to "release-name-hull-test-data-enabled-false-true"
* Test Object does not have key "data§test_disabled"
* Test Object has key "data§test_enabled" with value "This shall appear in configmap because enabled property is true"
* Test Object does not have key "data§test_disabled_transform"
* Test Object has key "data§test_enabled_transform" with value "This shall appear in configmap because enabled property is true via transformation"
* Test Object has key "data§test_enabled_missing" with value "This shall appear in configmap because enabled property is missing"

## Ordering
* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_order_test.hull.yaml" including suites "virtualfolderdata"
* Lint and Render values file "values_order_test.hull.yaml"

* Test object "release-name-hull-test-aaddheaders" does not exist
* Test object "release-name-hull-test-baddheaders" does not exist
* Set test object to "release-name-hull-test-caddheaders"
* Test Object has key "data§here" with value "some data"
* Test object "release-name-hull-test-daddheaders" does not exist

## Get Transformations
* Lint and Render
* Set test object to "release-name-hull-test-test-get-variants"
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
* Lint and Render
* Set test object to "release-name-hull-test-test-include-transformation"
* Test Object has key "data§include_name" with value "hull-test-test"
* Test Object has key "data§include_name_with_parent" with value "hull-test-test"
* Test Object has key "data§escape" with value "hull-test-split:by:colon"
* Test Object has key "data§chart_ref" with value "hull-test-1.29.0"
* Test Object has key "data§object_instance_key" with value "test-include-transformation"
* Test Object has key "data§object_type" with value "configmap"
* Test Object has key "data§object_instance_key_include" with value "hull-test-test-include-transformation"
* Test Object has key "data§object_type_include" with value "hull-test-configmap"
* Test Object has key "data§test_no_object_instance_key" with value ""
* Test Object has key "data§test_no_object_type" with value ""
* Test Object has key "metadata§labels§app.kubernetes.io/component" with value "overwritten_component"
* Test Object has key "metadata§annotations§app.kubernetes.io/component" with value "overwritten_component"

## Debug options
* Fail to render the templates for values file "values_broken_get_references.hull.yaml" to test execution folder because error contains "HULL failed with error HULL-GET-TRANSFORMATION-REFERENCE-INVALID: Element value_to_resolve_3 in path hull.config.specific.value_to_resolve_3 was not found"

* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_broken_get_references.hull.yaml" including suites "renderbrokenhullgettransformationreferences,virtualfolderdata"
* Lint and Render values file "values_broken_get_references.hull.yaml"

* Set test object to "release-name-hull-test-good-reference"
* Test Object has key "metadata§labels§test" with value "trans"

* Set test object to "release-name-hull-test-broken-parent-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element test in path hull.config.specific.test.value_to_resolve_1 was not found"

* Set test object to "release-name-hull-test-broken-leaf-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element value_to_resolve_3 in path hull.config.specific.value_to_resolve_3 was not found"

* Prepare test case "configmap" for kind "ConfigMap" including suites "rendernilwheninlineisnil,virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with value ""
* Test Object has key "data§nothing" with value "<nil>"
* Test Object has key "data§nil" with value "<nil>"


## Precedence
* Lint and Render
* Set test object to "release-name-hull-test-inline-precedence"
* Test Object has key "data§test1" with value "Inline Content"
* Test Object has key "data§test2" with value "Inline Content"

## Special cases
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with value ""

## Binary Data
* Lint and Render
* Set test object to "release-name-hull-test-binary-data-hull"
* Test Object has key "binaryData§binary_from_file" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

* Set test object to "release-name-hull-test-binary-data"
* Test Object has key "binaryData§binary" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

* Set test object to "release-name-hull-test-binary-data-mixed"
* Test Object has key "binaryData§binary" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"
* Test Object has key "binaryData§binary_from_file" with value "QÖÚ¼ˆ”¬µÖó¼ñƒ"

## Test serialization functions disabled
* Prepare default test case for this kind including suites "virtualfolderdata,serializationdisabled"
* Lint and Render
* Set test object to "release-name-hull-test-test-serializing"
* Test Object has key "data§test-inline-serialize-from-json-auto.yaml" with value of key "test-serialize-from-json-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yml" with value of key "test-serialize-from-json-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.json" with value of key "test-serialize-from-json-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yaml" with value of key "test-serialize-from-yaml-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yml" with value of key "test-serialize-from-yaml-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.json" with value of key "test-serialize-from-yaml-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yaml" with value of key "test-serialize-from-json-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yml" with value of key "test-serialize-from-json-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.json" with value of key "test-serialize-from-json-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yaml" with value of key "test-serialize-from-yaml-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yml" with value of key "test-serialize-from-yaml-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.json" with value of key "test-serialize-from-yaml-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"

## Test serialization functions
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-test-serializing"

* Test Object has key "data§test-inline-get-dict" with value of key "test-get-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-json" with value of key "test-get-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-none" with value of key "test-get-dict-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-prettyjson" with value of key "test-get-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-rawjson" with value of key "test-get-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-yaml" with value of key "test-get-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-string" with value of key "test-get-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list" with value of key "test-get-list" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-json" with value of key "test-get-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-none" with value of key "test-get-list-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-prettyjson" with value of key "test-get-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-rawjson" with value of key "test-get-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-yaml" with value of key "test-get-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-string" with value of key "test-get-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict" with value of key "test-include-code-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-json" with value of key "test-include-code-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-none" with value of key "test-include-code-dict-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-prettyjson" with value of key "test-include-code-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-rawjson" with value of key "test-include-code-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-yaml" with value of key "test-include-code-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-string" with value of key "test-include-code-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote" with value of key "test-include-code-dict-quote" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-json" with value of key "test-include-code-dict-quote-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-none" with value of key "test-include-code-dict-quote-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-prettyjson" with value of key "test-include-code-dict-quote-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-rawjson" with value of key "test-include-code-dict-quote-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-yaml" with value of key "test-include-code-dict-quote-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-string" with value of key "test-include-code-dict-quote-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty" with value of key "test-include-code-list-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-json" with value of key "test-include-code-list-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-none" with value of key "test-include-code-list-empty-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-prettyjson" with value of key "test-include-code-list-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-rawjson" with value of key "test-include-code-list-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-yaml" with value of key "test-include-code-list-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-string" with value of key "test-include-code-list-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty" with value of key "test-include-code-list-non-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-json" with value of key "test-include-code-list-non-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-none" with value of key "test-include-code-list-non-empty-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-prettyjson" with value of key "test-include-code-list-non-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-rawjson" with value of key "test-include-code-list-non-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-yaml" with value of key "test-include-code-list-non-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-string" with value of key "test-include-code-list-non-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-flow-dict" with value of key "test-include-flow-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-json" with value of key "test-serialize-from-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-none" with value of key "test-serialize-from-dict-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-prettyjson" with value of key "test-serialize-from-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-rawjson" with value of key "test-serialize-from-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-yaml" with value of key "test-serialize-from-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-string" with value of key "test-serialize-from-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-json" with value of key "test-serialize-from-json-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-none" with value of key "test-serialize-from-json-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-prettyjson" with value of key "test-serialize-from-json-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-rawjson" with value of key "test-serialize-from-json-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-yaml" with value of key "test-serialize-from-json-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-string" with value of key "test-serialize-from-json-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-json" with value of key "test-serialize-from-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-none" with value of key "test-serialize-from-list-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-prettyjson" with value of key "test-serialize-from-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-rawjson" with value of key "test-serialize-from-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-yaml" with value of key "test-serialize-from-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-string" with value of key "test-serialize-from-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-json" with value of key "test-serialize-from-yaml-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-prettyjson" with value of key "test-serialize-from-yaml-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-none" with value of key "test-serialize-from-yaml-none" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-rawjson" with value of key "test-serialize-from-yaml-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-yaml" with value of key "test-serialize-from-yaml-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-string" with value of key "test-serialize-from-yaml-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yaml" with value of key "test-serialize-from-json-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yml" with value of key "test-serialize-from-json-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.json" with value of key "test-serialize-from-json-auto.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yaml" with value of key "test-serialize-from-yaml-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yml" with value of key "test-serialize-from-yaml-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.json" with value of key "test-serialize-from-yaml-auto.json" from expected.yaml of suite "virtualfolderdata"

* Test Object has key "data§test-path-get-dict" with value of key "test-get-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-json" with value of key "test-get-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-prettyjson" with value of key "test-get-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-rawjson" with value of key "test-get-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-yaml" with value of key "test-get-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-string" with value of key "test-get-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list" with value of key "test-get-list" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-json" with value of key "test-get-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-prettyjson" with value of key "test-get-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-rawjson" with value of key "test-get-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-yaml" with value of key "test-get-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-string" with value of key "test-get-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict" with value of key "test-include-code-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-json" with value of key "test-include-code-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-prettyjson" with value of key "test-include-code-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-rawjson" with value of key "test-include-code-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-yaml" with value of key "test-include-code-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-string" with value of key "test-include-code-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote" with value of key "test-include-code-dict-quote" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-json" with value of key "test-include-code-dict-quote-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-prettyjson" with value of key "test-include-code-dict-quote-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-rawjson" with value of key "test-include-code-dict-quote-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-yaml" with value of key "test-include-code-dict-quote-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-string" with value of key "test-include-code-dict-quote-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty" with value of key "test-include-code-list-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-json" with value of key "test-include-code-list-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-prettyjson" with value of key "test-include-code-list-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-rawjson" with value of key "test-include-code-list-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-yaml" with value of key "test-include-code-list-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-string" with value of key "test-include-code-list-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty" with value of key "test-include-code-list-non-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-json" with value of key "test-include-code-list-non-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-prettyjson" with value of key "test-include-code-list-non-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-rawjson" with value of key "test-include-code-list-non-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-yaml" with value of key "test-include-code-list-non-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-string" with value of key "test-include-code-list-non-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-flow-dict" with value of key "test-include-flow-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-json" with value of key "test-serialize-from-json-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-prettyjson" with value of key "test-serialize-from-json-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-rawjson" with value of key "test-serialize-from-json-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-yaml" with value of key "test-serialize-from-json-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-string" with value of key "test-serialize-from-json-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-json" with value of key "test-serialize-from-yaml-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-prettyjson" with value of key "test-serialize-from-yaml-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-rawjson" with value of key "test-serialize-from-yaml-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-yaml" with value of key "test-serialize-from-yaml-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-string" with value of key "test-serialize-from-yaml-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yaml" with value of key "test-serialize-from-json-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yml" with value of key "test-serialize-from-json-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.json" with value of key "test-serialize-from-json-auto.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yaml" with value of key "test-serialize-from-yaml-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yml" with value of key "test-serialize-from-yaml-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.json" with value of key "test-serialize-from-yaml-auto.json" from expected.yaml of suite "virtualfolderdata"

## Documentation example for ConfigMap and Secret serialization
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-doc-json-serialization-examples"

* Test Object has key "data§no-serialization.json" with value of key "doc-json-serialization-examples-unchanged.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§implicit-from-dictionary.json" with value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§implicit-from-get-transformation.json" with value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-from-dictionary" with value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-from-yaml.yaml" with value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-none-conversion.json" with value of key "doc-json-serialization-examples-unchanged.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§simple-string" with value of key "simple-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§app-configuration-yaml" with value of key "app-configuration-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§app-configuration-json" with value of key "app-configuration-json" from expected.yaml of suite "virtualfolderdata"

## Error Checking
* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_error_handling_missing_path.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_missing_path.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING: ConfigMap/virtual-folder-path-invalid/path/invalid(files/nothing-here)"

* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_error_handling_invalid_inline.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_invalid_inline.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-INLINE-INVALID: ConfigMap/virtual-folder-inline-invalid/inline/invalid"

* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_error_handling_null_inline.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_null_inline.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-INLINE-INVALID: ConfigMap/virtual-folder-inline-null/inline/nothing"

* Prepare test case "configmap" for kind "ConfigMap" with test chart "hull-test" and values file "values_error_handling_disabled.hull.yaml" including suites "virtualfolderdata"
* Lint and Render values file "values_error_handling_disabled.hull.yaml"

## Non-Hull Values access
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-non-hull-values-access"

* Test Object has key "data§inline-issue-288-ht-tpl" with value of key "issue-288-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-tpl" with value of key "subdict-access-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-ht-get" with value of key "issue-288-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get" with value of key "subdict-access-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-json" with value of key "subdict-access-ht-get-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-prettyjson" with value of key "subdict-access-ht-get-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-rawjson" with value of key "subdict-access-ht-get-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-yaml" with value of key "subdict-access-ht-get-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-string" with value of key "subdict-access-ht-get-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-dollar" with value of key "issue-288-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-dollar" with value of key "subdict-access-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-dot" with value of key "issue-288-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-dot" with value of key "subdict-access-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-ht-tpl" with value of key "issue-288-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-tpl" with value of key "subdict-access-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-ht-get" with value of key "issue-288-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get" with value of key "subdict-access-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-json" with value of key "subdict-access-ht-get-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-prettyjson" with value of key "subdict-access-ht-get-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-rawjson" with value of key "subdict-access-ht-get-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-yaml" with value of key "subdict-access-ht-get-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-string" with value of key "subdict-access-ht-get-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-dollar" with value of key "issue-288-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-dollar" with value of key "subdict-access-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-dot" with value of key "issue-288-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-dot" with value of key "subdict-access-dot" from expected.yaml of suite "virtualfolderdata"

___

* Clean the test execution folder