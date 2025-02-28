# BackendLBPolicy

Test creation of objects and features.

* Prepare default test case for kind "BackendLBPolicy"

## Render and Validate

* Lint and Render
* Expected number of "16" objects were rendered on top of basic objects count
* Validate with additional schemas in subfolder "gateway-api"

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
* Test Object has key "spec§targetRefs§1§name" with value "name2"
* Test Object has key "spec§targetRefs§1§group" with value "group2"
* Test Object has key "spec§targetRefs§1§kind" with value "kind2"
* Test Object has key "spec§sessionPersistence§sessionName" with value "lbsession"
* Test Object has key "spec§sessionPersistence§absoluteTimeout" with value "1m"
* Test Object has key "spec§sessionPersistence§idleTimeout" with value "2m"
* Test Object has key "spec§sessionPersistence§type" with value "Cookie"
* Test Object has key "spec§sessionPersistence§cookieConfig§lifetimeType" with value "Permanent"

___

* Clean the test execution folder