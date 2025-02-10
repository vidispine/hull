# BackendTLSPolicy

Test creation of objects and features.

* Prepare default test case for kind "BackendTLSPolicy"

## Render and Validate

* Lint and Render
* Expected number of "16" objects were rendered on top of basic objects count

## Metadata

* Check basic metadata functionality

## Dynamic Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "spec§targetRefs" with array value that has "1" items
* Test Object has key "spec§targetRefs§0§name" with value "name"
* Test Object has key "spec§targetRefs§0§group" with value "group"
* Test Object has key "spec§targetRefs§0§kind" with value "kind"

* Set test object to "release-name-hull-test-dictionary"
* Test Object has key "spec§targetRefs" with array value that has "1" items
* Test Object has key "spec§targetRefs§0§name" with value "name"
* Test Object has key "spec§targetRefs§0§group" with value "group"
* Test Object has key "spec§targetRefs§0§kind" with value "kind"

## Full Example
* Lint and Render
* Set test object to "release-name-hull-test-full-example"
* Test Object has key "spec§targetRefs" with array value that has "2" items
* Test Object has key "spec§targetRefs§0§name" with value "name1"
* Test Object has key "spec§targetRefs§0§group" with value "group1"
* Test Object has key "spec§targetRefs§0§kind" with value "kind1"
* Test Object has key "spec§targetRefs§0§sectionName" with value "testsection"
* Test Object has key "spec§targetRefs§1§name" with value "name2"
* Test Object has key "spec§targetRefs§1§group" with value "group2"
* Test Object has key "spec§targetRefs§1§kind" with value "kind2"
* Test Object has key "spec§validation§hostname" with value "myhost"
* Test Object has key "spec§validation§wellKnownCACertificates" with value "System"
* Test Object has key "spec§validation§subjectAltNames§0§type" with value "Hostname"
* Test Object has key "spec§validation§subjectAltNames§0§hostname" with value "salt"
* Test Object has key "spec§validation§subjectAltNames§1§type" with value "URI"
* Test Object has key "spec§validation§subjectAltNames§1§uri" with value "http://sanuri"
* Test Object has key "spec§options§bli" with value "blu"
* Test Object has key "spec§options§bla" with value "blo"
___

* Clean the test execution folder