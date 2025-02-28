# GRPCRoute

Test creation of objects and features.

* Prepare default test case for kind "GRPCRoute"

## Render and Validate

* Lint and Render
* Expected number of "1" objects were rendered on top of basic objects count
* Validate with additional schemas in subfolder "gateway-api"

## Metadata

* Check basic metadata functionality

## Full Example
* Lint and Render
* Set test object to "release-name-hull-test-full-example"
* Test Object has key "spec§parentRefs§0§group" with value "group1"
* Test Object has key "spec§parentRefs§0§kind" with value "kind1"
* Test Object has key "spec§parentRefs§0§namespace" with value "namespace1"
* Test Object has key "spec§parentRefs§0§name" with value "name1"
* Test Object has key "spec§parentRefs§0§sectionName" with value "testsection1"
* Test Object has key "spec§parentRefs§0§port" with integer value "1"
* Test Object has key "spec§parentRefs§1§group" with value "group2"
* Test Object has key "spec§parentRefs§1§kind" with value "kind2"
* Test Object has key "spec§parentRefs§1§namespace" with value "namespace2"
* Test Object has key "spec§parentRefs§1§name" with value "name2"
* Test Object has key "spec§parentRefs§1§sectionName" with value "testsection2"
* Test Object has key "spec§parentRefs§1§port" with integer value "2"
* Test Object has key "spec§hostnames§0" with value "host1"
* Test Object has key "spec§hostnames§1" with value "host2"
* Test Object has key "spec§rules§0§name" with value "one"
* Test Object has key "spec§rules§0§sessionPersistence§absoluteTimeout" with value "456s"
* Test Object has key "spec§rules§0§sessionPersistence§type" with value "Cookie"
* Test Object has key "spec§rules§0§sessionPersistence§idleTimeout" with value "123s"
* Test Object has key "spec§rules§0§sessionPersistence§sessionName" with value "sessionname"
* Test Object has key "spec§rules§0§sessionPersistence§cookieConfig§lifetimeType" with value "Permanent"
* Test Object has key "spec§rules§0§matches§0§method§type" with value "Exact"
* Test Object has key "spec§rules§0§matches§0§method§service" with value "matchservice1"
* Test Object has key "spec§rules§0§matches§0§method§method" with value "matchmethod1"
* Test Object has key "spec§rules§0§matches§0§headers§0§name" with value "firstheader"
* Test Object has key "spec§rules§0§matches§0§headers§0§type" with value "Exact"
* Test Object has key "spec§rules§0§matches§0§headers§0§value" with value "someheadervalue1"
* Test Object has key "spec§rules§0§matches§1§headers§0§name" with value "secheader"
* Test Object has key "spec§rules§0§matches§1§headers§0§type" with value "Exact"
* Test Object has key "spec§rules§0§matches§1§headers§0§value" with value "secheadervalue2"
* Test Object has key "spec§rules§0§filters§0§type" with value "ExtensionRef"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§set§0§name" with value "Accept1"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§set§0§value" with value "json1"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§set§1§name" with value "Accept2"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§set§1§value" with value "json2"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§add§0§name" with value "Accept3"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§add§0§value" with value "json3"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§add§1§name" with value "Accept4"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§add§1§value" with value "json4"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§remove§0" with value "oldheader1"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§remove§1" with value "oldheader2"
* Test Object has key "spec§rules§0§filters§0§requestHeaderModifier§set§0§name" with value "Accept1"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§set§0§value" with value "json1"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§set§1§name" with value "Accept2"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§set§1§value" with value "json2"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§add§0§name" with value "Accept3"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§add§0§value" with value "json3"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§add§1§name" with value "Accept4"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§add§1§value" with value "json4"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§remove§0" with value "oldheader1"
* Test Object has key "spec§rules§0§filters§0§responseHeaderModifier§remove§1" with value "oldheader2"
* Test Object has key "spec§rules§0§filters§0§requestMirror§backendRef§group" with value "group1"
* Test Object has key "spec§rules§0§filters§0§requestMirror§backendRef§kind" with value "kind1"
* Test Object has key "spec§rules§0§filters§0§requestMirror§backendRef§namespace" with value "namespace1"
* Test Object has key "spec§rules§0§filters§0§requestMirror§backendRef§name" with value "name1"
* Test Object has key "spec§rules§0§filters§0§requestMirror§backendRef§port" with integer value "1"
* Test Object has key "spec§rules§0§filters§0§requestMirror§percent" with integer value "66"
* Test Object has key "spec§rules§0§filters§0§requestMirror§fraction§numerator" with integer value "11"
* Test Object has key "spec§rules§0§filters§0§requestMirror§fraction§denominator" with integer value "22"
* Test Object has key "spec§rules§0§filters§0§extensionRef§group" with value "group1"
* Test Object has key "spec§rules§0§filters§0§extensionRef§kind" with value "kind1"
* Test Object has key "spec§rules§0§filters§0§extensionRef§name" with value "name1"
* Test Object has key "spec§rules§0§backendRefs§0§group" with value "group1"
* Test Object has key "spec§rules§0§backendRefs§0§kind" with value "kind1"
* Test Object has key "spec§rules§0§backendRefs§0§namespace" with value "namespace1"
* Test Object has key "spec§rules§0§backendRefs§0§name" with value "name1"
* Test Object has key "spec§rules§0§backendRefs§0§weight" with integer value "965"
* Test Object has key "spec§rules§0§backendRefs§0§port" with integer value "1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§type" with value "ExtensionRef"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§set§0§name" with value "Accept1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§set§0§value" with value "json1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§set§1§name" with value "Accept2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§set§1§value" with value "json2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§add§0§name" with value "Accept3"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§add§0§value" with value "json3"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§add§1§name" with value "Accept4"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§add§1§value" with value "json4"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§remove§0" with value "oldheader1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§remove§1" with value "oldheader2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestHeaderModifier§set§0§name" with value "Accept1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§set§0§value" with value "json1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§set§1§name" with value "Accept2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§set§1§value" with value "json2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§add§0§name" with value "Accept3"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§add§0§value" with value "json3"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§add§1§name" with value "Accept4"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§add§1§value" with value "json4"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§remove§0" with value "oldheader1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§responseHeaderModifier§remove§1" with value "oldheader2"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§backendRef§group" with value "group1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§backendRef§kind" with value "kind1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§backendRef§namespace" with value "namespace1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§backendRef§name" with value "name1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§backendRef§port" with integer value "1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§percent" with integer value "66"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§fraction§numerator" with integer value "11"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§requestMirror§fraction§denominator" with integer value "22"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§extensionRef§group" with value "group1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§extensionRef§kind" with value "kind1"
* Test Object has key "spec§rules§0§backendRefs§0§filters§0§extensionRef§name" with value "name1"

___

* Clean the test execution folder