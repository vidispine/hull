# Secrets

Test creation of objects and features.

* Prepare default test case for kind "Secret"
* Prepare default test case for this kind including suites "virtualfolderdata,globalmetadata,objecttypemetadata"

## Render and Validate
* Lint and Render
* Expected number of "25" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Defaulting
* Lint and Render
* All test objects have key "data§default_inline_1" with Base64 encoded value of "Default Inline 1"
* All test objects have key "data§default_file_1.json" with Base64 encoded value of key "default_file_1.json" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-defaults-no-overwrite"
* Test Object has key "data§default_inline_2" with Base64 encoded value of "Default Inline 2"
* Test Object has key "data§default_file_2.yaml" with Base64 encoded value of "name: i am default_file_2.yaml"

* Set test object to "release-name-hull-test-defaults-overwrite"
* Test Object has key "data§default_inline_2" with Base64 encoded value of "Concrete Inline 2"
* Test Object has key "data§default_file_2.yaml" with Base64 encoded value of "name: i am concrete_file_2.yaml"

## Templating
* Lint and Render
* Set test object to "release-name-hull-test-no-templating"
* Test Object has key "data§concrete_file_3_templated.yaml" with Base64 encoded value of "name: i am concrete_file_3.yaml\ntemplating: General Custom Label 1"
* Test Object has key "data§concrete_file_3_untemplated.yaml" with Base64 encoded value of key "concrete_file_3_untemplated.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline_templated.txt" with Base64 encoded value of "This is an inline with a pointer to a transformation."
* Test Object has key "data§inline_untemplated.txt" with Base64 encoded value of "This is an inline with a pointer to a \{\{ .Values.hull.config.specific.resolve_me \}\}."

## Transformation
* Lint and Render
* Set test object to "release-name-hull-test-transformation-resolved"
* Test Object has key "data§concrete_file_4_resolved.txt" with Base64 encoded value of "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with Base64 encoded value of "transformation = transformation"
* Set test object to "release-name-hull-test-transformation-resolved-short"
* Test Object has key "data§concrete_file_4_resolved.txt" with Base64 encoded value of "This is a text file with a pointer to a transformation."
* Test Object has key "data§equal_sign_preservation" with Base64 encoded value of "transformation = transformation"

## Enable Data 
* Lint and Render
* Set test object to "release-name-hull-test-data-enabled-false-true"
* Test Object does not have key "data§test_disabled"
* Test Object has key "data§test_enabled" with Base64 encoded value of "This shall appear in secret because enabled property is true"
* Test Object does not have key "data§test_disabled_transform"
* Test Object has key "data§test_enabled_transform" with Base64 encoded value of "This shall appear in secret because enabled property is true via transformation"
* Test Object has key "data§test_enabled_missing" with Base64 encoded value of "This shall appear in secret because enabled property is missing"

## Ordering
* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_order_test.hull.yaml" including suites "virtualfolderdata"
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
* Test Object has key "data§key_with_dots_in_it" with Base64 encoded value of "hello dots!"

## Include Transformation 
* Lint and Render
* Set test object to "release-name-hull-test-test-include-transformation"
* Test Object has key "data§include_name" with Base64 encoded value of "hull-test-test"
* Test Object has key "data§include_name_with_parent" with Base64 encoded value of "hull-test-test"
* Test Object has key "data§escape" with Base64 encoded value of "hull-test-split:by:colon"
* Test Object has key "data§chart_ref" with Base64 encoded value of "hull-test-<K8S_MAJOR_VERSION>.0"
* Test Object has key "data§object_instance_key" with Base64 encoded value of "test-include-transformation"
* Test Object has key "data§object_type" with Base64 encoded value of "secret"
* Test Object has key "data§object_instance_key_include" with Base64 encoded value of "hull-test-test-include-transformation"
* Test Object has key "data§object_type_include" with Base64 encoded value of "hull-test-secret"
* Test Object has key "data§test_no_object_instance_key" with Base64 encoded value of ""
* Test Object has key "data§test_no_object_type" with Base64 encoded value of ""
* Test Object has key "metadata§labels§app.kubernetes.io/component" with value "overwritten_component"
* Test Object has key "metadata§annotations§app.kubernetes.io/component" with value "overwritten_component"

## Debug options
* Fail to render the templates for values file "values_broken_get_references.hull.yaml" to test execution folder because error contains "HULL failed with error HULL-GET-TRANSFORMATION-REFERENCE-INVALID: Element value_to_resolve_3 in path hull.config.specific.value_to_resolve_3 was not found"

* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_broken_get_references.hull.yaml" including suites "renderbrokenhullgettransformationreferences,virtualfolderdata"
* Lint and Render values file "values_broken_get_references.hull.yaml"

* Set test object to "release-name-hull-test-good-reference"
* Test Object has key "metadata§labels§test" with value "trans"

* Set test object to "release-name-hull-test-broken-parent-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element test in path hull.config.specific.test.value_to_resolve_1 was not found"

* Set test object to "release-name-hull-test-broken-leaf-reference"
* Test Object has key "metadata§labels§test" with value "BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element value_to_resolve_3 in path hull.config.specific.value_to_resolve_3 was not found"

* Prepare test case "secret" for kind "Secret" including suites "rendernilwheninlineisnil,virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with Base64 encoded value of ""
* Test Object has key "data§nothing" with Base64 encoded value of "<nil>"
* Test Object has key "data§nil" with Base64 encoded value of "<nil>"


## Precedence
* Lint and Render
* Set test object to "release-name-hull-test-inline-precedence"
* Test Object has key "data§test1" with Base64 encoded value of "Inline Content"
* Test Object has key "data§test2" with Base64 encoded value of "Inline Content"

## Special cases
* Lint and Render
* Set test object to "release-name-hull-test-special-cases"
* Test Object has key "data§empty" with Base64 encoded value of ""

## Test serialization functions disabled
* Prepare default test case for this kind including suites "virtualfolderdata,serializationdisabled"
* Lint and Render
* Set test object to "release-name-hull-test-test-serializing"
* Test Object has key "data§test-inline-serialize-from-json-auto.yaml" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yml" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.json" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yaml" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yml" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.json" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yaml" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yml" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.json" with Base64 encoded value of key "test-serialize-from-json-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yaml" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yml" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.json" with Base64 encoded value of key "test-serialize-from-yaml-auto-disabled.json" from expected.yaml of suite "virtualfolderdata"

## Test serialization functions
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-test-serializing"

* Test Object has key "data§test-inline-get-dict" with Base64 encoded value of key "test-get-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-json" with Base64 encoded value of key "test-get-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-prettyjson" with Base64 encoded value of key "test-get-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-rawjson" with Base64 encoded value of key "test-get-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-yaml" with Base64 encoded value of key "test-get-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-dict-string" with Base64 encoded value of key "test-get-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list" with Base64 encoded value of key "test-get-list" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-json" with Base64 encoded value of key "test-get-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-prettyjson" with Base64 encoded value of key "test-get-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-rawjson" with Base64 encoded value of key "test-get-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-yaml" with Base64 encoded value of key "test-get-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-get-list-string" with Base64 encoded value of key "test-get-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict" with Base64 encoded value of key "test-include-code-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-json" with Base64 encoded value of key "test-include-code-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-prettyjson" with Base64 encoded value of key "test-include-code-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-rawjson" with Base64 encoded value of key "test-include-code-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-yaml" with Base64 encoded value of key "test-include-code-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-string" with Base64 encoded value of key "test-include-code-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote" with Base64 encoded value of key "test-include-code-dict-quote" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-json" with Base64 encoded value of key "test-include-code-dict-quote-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-prettyjson" with Base64 encoded value of key "test-include-code-dict-quote-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-rawjson" with Base64 encoded value of key "test-include-code-dict-quote-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-yaml" with Base64 encoded value of key "test-include-code-dict-quote-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-dict-quote-string" with Base64 encoded value of key "test-include-code-dict-quote-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty" with Base64 encoded value of key "test-include-code-list-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-json" with Base64 encoded value of key "test-include-code-list-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-prettyjson" with Base64 encoded value of key "test-include-code-list-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-rawjson" with Base64 encoded value of key "test-include-code-list-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-yaml" with Base64 encoded value of key "test-include-code-list-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-empty-string" with Base64 encoded value of key "test-include-code-list-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty" with Base64 encoded value of key "test-include-code-list-non-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-json" with Base64 encoded value of key "test-include-code-list-non-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-prettyjson" with Base64 encoded value of key "test-include-code-list-non-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-rawjson" with Base64 encoded value of key "test-include-code-list-non-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-yaml" with Base64 encoded value of key "test-include-code-list-non-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-code-list-non-empty-string" with Base64 encoded value of key "test-include-code-list-non-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-include-flow-dict" with Base64 encoded value of key "test-include-flow-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-json" with Base64 encoded value of key "test-serialize-from-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-prettyjson" with Base64 encoded value of key "test-serialize-from-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-rawjson" with Base64 encoded value of key "test-serialize-from-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-yaml" with Base64 encoded value of key "test-serialize-from-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-dict-string" with Base64 encoded value of key "test-serialize-from-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-json" with Base64 encoded value of key "test-serialize-from-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-prettyjson" with Base64 encoded value of key "test-serialize-from-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-rawjson" with Base64 encoded value of key "test-serialize-from-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-yaml" with Base64 encoded value of key "test-serialize-from-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-list-string" with Base64 encoded value of key "test-serialize-from-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-json" with Base64 encoded value of key "test-serialize-from-json-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-prettyjson" with Base64 encoded value of key "test-serialize-from-json-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-rawjson" with Base64 encoded value of key "test-serialize-from-json-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-yaml" with Base64 encoded value of key "test-serialize-from-json-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-string" with Base64 encoded value of key "test-serialize-from-json-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-json" with Base64 encoded value of key "test-serialize-from-yaml-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-prettyjson" with Base64 encoded value of key "test-serialize-from-yaml-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-rawjson" with Base64 encoded value of key "test-serialize-from-yaml-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-yaml" with Base64 encoded value of key "test-serialize-from-yaml-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-string" with Base64 encoded value of key "test-serialize-from-yaml-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yaml" with Base64 encoded value of key "test-serialize-from-json-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.yml" with Base64 encoded value of key "test-serialize-from-json-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-json-auto.json" with Base64 encoded value of key "test-serialize-from-json-auto.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yaml" with Base64 encoded value of key "test-serialize-from-yaml-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.yml" with Base64 encoded value of key "test-serialize-from-yaml-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-inline-serialize-from-yaml-auto.json" with Base64 encoded value of key "test-serialize-from-yaml-auto.json" from expected.yaml of suite "virtualfolderdata"

* Test Object has key "data§test-path-get-dict" with Base64 encoded value of key "test-get-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-json" with Base64 encoded value of key "test-get-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-prettyjson" with Base64 encoded value of key "test-get-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-rawjson" with Base64 encoded value of key "test-get-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-yaml" with Base64 encoded value of key "test-get-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-dict-string" with Base64 encoded value of key "test-get-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list" with Base64 encoded value of key "test-get-list" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-json" with Base64 encoded value of key "test-get-list-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-prettyjson" with Base64 encoded value of key "test-get-list-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-rawjson" with Base64 encoded value of key "test-get-list-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-yaml" with Base64 encoded value of key "test-get-list-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-get-list-string" with Base64 encoded value of key "test-get-list-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict" with Base64 encoded value of key "test-include-code-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-json" with Base64 encoded value of key "test-include-code-dict-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-prettyjson" with Base64 encoded value of key "test-include-code-dict-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-rawjson" with Base64 encoded value of key "test-include-code-dict-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-yaml" with Base64 encoded value of key "test-include-code-dict-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-string" with Base64 encoded value of key "test-include-code-dict-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote" with Base64 encoded value of key "test-include-code-dict-quote" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-json" with Base64 encoded value of key "test-include-code-dict-quote-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-prettyjson" with Base64 encoded value of key "test-include-code-dict-quote-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-rawjson" with Base64 encoded value of key "test-include-code-dict-quote-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-yaml" with Base64 encoded value of key "test-include-code-dict-quote-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-dict-quote-string" with Base64 encoded value of key "test-include-code-dict-quote-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty" with Base64 encoded value of key "test-include-code-list-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-json" with Base64 encoded value of key "test-include-code-list-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-prettyjson" with Base64 encoded value of key "test-include-code-list-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-rawjson" with Base64 encoded value of key "test-include-code-list-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-yaml" with Base64 encoded value of key "test-include-code-list-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-empty-string" with Base64 encoded value of key "test-include-code-list-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty" with Base64 encoded value of key "test-include-code-list-non-empty" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-json" with Base64 encoded value of key "test-include-code-list-non-empty-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-prettyjson" with Base64 encoded value of key "test-include-code-list-non-empty-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-rawjson" with Base64 encoded value of key "test-include-code-list-non-empty-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-yaml" with Base64 encoded value of key "test-include-code-list-non-empty-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-code-list-non-empty-string" with Base64 encoded value of key "test-include-code-list-non-empty-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-include-flow-dict" with Base64 encoded value of key "test-include-flow-dict" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-json" with Base64 encoded value of key "test-serialize-from-json-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-prettyjson" with Base64 encoded value of key "test-serialize-from-json-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-rawjson" with Base64 encoded value of key "test-serialize-from-json-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-yaml" with Base64 encoded value of key "test-serialize-from-json-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-string" with Base64 encoded value of key "test-serialize-from-json-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-json" with Base64 encoded value of key "test-serialize-from-yaml-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-prettyjson" with Base64 encoded value of key "test-serialize-from-yaml-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-rawjson" with Base64 encoded value of key "test-serialize-from-yaml-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-yaml" with Base64 encoded value of key "test-serialize-from-yaml-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-string" with Base64 encoded value of key "test-serialize-from-yaml-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yaml" with Base64 encoded value of key "test-serialize-from-json-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.yml" with Base64 encoded value of key "test-serialize-from-json-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-json-auto.json" with Base64 encoded value of key "test-serialize-from-json-auto.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yaml" with Base64 encoded value of key "test-serialize-from-yaml-auto.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.yml" with Base64 encoded value of key "test-serialize-from-yaml-auto.yml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§test-path-serialize-from-yaml-auto.json" with Base64 encoded value of key "test-serialize-from-yaml-auto.json" from expected.yaml of suite "virtualfolderdata"

## Documentation example for ConfigMap and Secret serialization
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-doc-json-serialization-examples"

* Test Object has key "data§no-serialization.json" with Base64 encoded value of key "doc-json-serialization-examples-unchanged.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§implicit-from-dictionary.json" with Base64 encoded value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§implicit-from-get-transformation.json" with Base64 encoded value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-from-dictionary" with Base64 encoded value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-from-yaml.yaml" with Base64 encoded value of key "doc-json-serialization-examples-serialized.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§explicit-none-conversion.json" with Base64 encoded value of key "doc-json-serialization-examples-unchanged.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§simple-string" with Base64 encoded value of key "simple-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§app-configuration-yaml" with Base64 encoded value of key "app-configuration-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§app-configuration-json" with Base64 encoded value of key "app-configuration-json" from expected.yaml of suite "virtualfolderdata"

## Error Checking
* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_error_handling_missing_path.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_missing_path.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING: Secret/virtual-folder-path-invalid/path/invalid(files/nothing-here)"

* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_error_handling_invalid_inline.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_invalid_inline.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-INLINE-INVALID: Secret/virtual-folder-inline-invalid/inline/invalid"

* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_error_handling_null_inline.hull.yaml" including suites "virtualfolderdata"
* Fail to render the templates for values file "values_error_handling_null_inline.hull.yaml" to test execution folder because error contains "HULL failed with error VIRTUAL-FOLDER-DATA-INLINE-INVALID: Secret/virtual-folder-inline-null/inline/nothing"

* Prepare test case "secret" for kind "Secret" with test chart "hull-test" and values file "values_error_handling_disabled.hull.yaml" including suites "virtualfolderdata"
* Lint and Render values file "values_error_handling_disabled.hull.yaml"

## Non-Hull Values access
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-non-hull-values-access"

* Test Object has key "data§inline-issue-288-ht-tpl" with Base64 encoded value of key "issue-288-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-tpl" with Base64 encoded value of key "subdict-access-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-ht-get" with Base64 encoded value of key "issue-288-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get" with Base64 encoded value of key "subdict-access-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-json" with Base64 encoded value of key "subdict-access-ht-get-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-prettyjson" with Base64 encoded value of key "subdict-access-ht-get-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-rawjson" with Base64 encoded value of key "subdict-access-ht-get-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-yaml" with Base64 encoded value of key "subdict-access-ht-get-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-ht-get-string" with Base64 encoded value of key "subdict-access-ht-get-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-dollar" with Base64 encoded value of key "issue-288-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-dollar" with Base64 encoded value of key "subdict-access-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-issue-288-dot" with Base64 encoded value of key "issue-288-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§inline-subdict-access-dot" with Base64 encoded value of key "subdict-access-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-ht-tpl" with Base64 encoded value of key "issue-288-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-tpl" with Base64 encoded value of key "subdict-access-ht-tpl" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-ht-get" with Base64 encoded value of key "issue-288-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get" with Base64 encoded value of key "subdict-access-ht-get" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-json" with Base64 encoded value of key "subdict-access-ht-get-json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-prettyjson" with Base64 encoded value of key "subdict-access-ht-get-prettyjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-rawjson" with Base64 encoded value of key "subdict-access-ht-get-rawjson" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-yaml" with Base64 encoded value of key "subdict-access-ht-get-yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-ht-get-string" with Base64 encoded value of key "subdict-access-ht-get-string" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-dollar" with Base64 encoded value of key "issue-288-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-dollar" with Base64 encoded value of key "subdict-access-dollar" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-issue-288-dot" with Base64 encoded value of key "issue-288-dot" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§path-subdict-access-dot" with Base64 encoded value of key "subdict-access-dot" from expected.yaml of suite "virtualfolderdata"

## GLOB loading files
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render
* Set test object to "release-name-hull-test-test-glob-import"

* Test Object has key "data§default_file_1.json" with Base64 encoded value of key "default_file_1.json" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§default_file_2.yaml" with Base64 encoded value of key "default_file_2.yaml" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§default_inline_1" with Base64 encoded value of "Default Inline 1"
* Test Object has key "data§default_inline_2" with Base64 encoded value of "Default Inline 2"
* Test Object has key "data§code-java-simple.java" with Base64 encoded value of key "code-java-simple.java" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§code-java-medium.java" with Base64 encoded value of key "code-java-medium.java" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§code-java-complex.java" with Base64 encoded value of key "code-java-complex.java" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-test-glob-import-template"
* Test Object has key "data§templated-code.java" with Base64 encoded value of key "templated-code-template.java" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§templated-json.json" with Base64 encoded value of key "templated-json-template.json" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-test-glob-import-no-template"
* Test Object has key "data§templated-code.java" with Base64 encoded value of key "templated-code-no-template.java" from expected.yaml of suite "virtualfolderdata"
* Test Object has key "data§templated-json.json" with Base64 encoded value of key "templated-json-no-template.json" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-test-glob-import-template-serialize"
* Test Object has key "data§templated-json.json" with Base64 encoded value of key "templated-json-template-serialize.yaml" from expected.yaml of suite "virtualfolderdata"

* Set test object to "release-name-hull-test-test-glob-import-no-template-serialize"
* Test Object has key "data§templated-json.json" with Base64 encoded value of key "templated-json-no-template-serialize.yaml" from expected.yaml of suite "virtualfolderdata"

## Secret Types
* Lint and Render
* Set test object to "release-name-hull-test-type-default"
* Test Object has key "type" with value "Opaque"

* Set test object to "release-name-hull-test-type-opaque"
* Test Object has key "type" with value "Opaque"

* Set test object to "release-name-hull-test-type-dockerconfigjson"
* Test Object has key "type" with value "kubernetes.io/dockerconfigjson"

* Set test object to "release-name-hull-test-type-serviceaccounttoken"
* Test Object has key "type" with value "kubernetes.io/service-account-token"

* Set test object to "release-name-hull-test-type-custom"
* Test Object has key "type" with value "custom.com/secret-type"

## Verify sources are not muddled together
* Prepare default test case for this kind including suites "virtualfolderdata"
* Lint and Render values file "secret_sources_seperated.values.hull.yaml"

* Set test object to "release-name-hull-test-auth"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-100"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-1"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-2"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-3"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-4"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-5"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-6"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-7"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-8"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-9"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-custom-installation-files-10"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-80"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "release-name-hull-test-authservice"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-10"
* Test Object has key "metadata§annotations§helm.sh/hook-delete-policy" with value "before-hook-creation"
* Test Object has key "data§dummy" with Base64 encoded value of "Just another dummy text"

* Set test object to "shared-cert"

* Set test object to "release-name-hull-test-keycloak-user"
* Test Object does not have key "metadata§annotations§helm.sh/hook"
* Test Object does not have key "metadata§annotations§helm.sh/hook-weight"
* Test Object does not have key "metadata§annotations§helm.sh/hook-delete-policy"
* Test Object has key "data§KEYCLOAK_ADMIN" with Base64 encoded value of "admin"
* Test Object has key "data§KEYCLOAK_ADMIN_PASSWORD" with Base64 encoded value of ""
* Test Object has key "data§KEYCLOAK_MANAGEMENT_USER" with Base64 encoded value of "manager"
* Test Object has key "data§KEYCLOAK_MANAGEMENT_PASSWORD" with Base64 encoded value of ""
* Test Object has key "data§VIDISPINE_REALM_ADMIN" with Base64 encoded value of "admin"
* Test Object has key "data§VIDISPINE_REALM_ADMIN_PASSWORD" with Base64 encoded value of ""

## Preencoded Secret data
* Lint and Render
* Set test object to "release-name-hull-test-encoding"
* Test Object has key "data§text_unencoded_encode_inline" with Base64 encoded value of "This text is encoded in Base64 format"
* Test Object has key "data§text_encoded_encode_inline" with Base64 encoded value of "VGhpcyB0ZXh0IGlzIGVuY29kZWQgaW4gQmFzZTY0IGZvcm1hdA=="
* Test Object has key "data§text_encoded_unencode_inline" with Base64 encoded value of "This text is encoded in Base64 format"
* Test Object has key "data§binary_unencoded_encode_inline" with Base64 encoded value of "QÖÚ¼ˆ”¬µÖó¼ñƒ"
* Test Object has key "data§binary_encoded_encode_inline" with Base64 encoded value of "UcOWw5rCvMuG4oCdwqzCtcOWw7PCvMOxxpI="
* Test Object has key "data§binary_encoded_unencode_inline" with Base64 encoded value of "QÖÚ¼ˆ”¬µÖó¼ñƒ"
* Test Object has key "data§text_unencoded_encode_path" with Base64 encoded value of "This text is encoded in Base64 format"
* Test Object has key "data§text_encoded_encode_path" with Base64 encoded value of "VGhpcyB0ZXh0IGlzIGVuY29kZWQgaW4gQmFzZTY0IGZvcm1hdA=="
* Test Object has key "data§text_encoded_unencode_path" with Base64 encoded value of "This text is encoded in Base64 format"
* Test Object has key "data§binary_unencoded_encode_path" with Base64 encoded value of "QÖÚ¼ˆ”¬µÖó¼ñƒ"
* Test Object has key "data§binary_encoded_encode_path" with Base64 encoded value of "UcOWw5rCvMuG4oCdwqzCtcOWw7PCvMOxxpI="
* Test Object has key "data§binary_encoded_unencode_path" with Base64 encoded value of "QÖÚ¼ˆ”¬µÖó¼ñƒ"

* Clean the test execution folder