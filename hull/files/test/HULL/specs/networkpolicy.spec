# NetworkPolicy

Test creation of objects and features.

* Prepare default test case for kind "NetworkPolicy"

## Render and Validate
* Render
* Expected number of "8" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Data

* Render

* Set test object to "release-name-hull-test-standard"
* Test Object has key "spec§egress§0§ports§0§port" with integer value "80"
* Test Object has key "spec§egress§0§ports§0§protocol" with value "TCP"
* Test Object has key "spec§egress§0§ports§1§port" with value "udp-out"
* Test Object has key "spec§egress§0§ports§1§protocol" with value "UDP"
* Test Object has key "spec§egress§0§to§0§ipBlock§cidr" with value "192.168.1.1/24"
* Test Object has key "spec§ingress§0§ports§0§port" with integer value "89"
* Test Object has key "spec§ingress§0§ports§0§protocol" with value "TCP"
* Test Object has key "spec§ingress§0§ports§1§port" with value "udp-in"
* Test Object has key "spec§ingress§0§ports§1§protocol" with value "UDP"
* Test Object has key "spec§ingress§0§from§0§ipBlock§cidr" with value "192.168.1.1/1"
* Test Object has key "spec§policyTypes§0" with value "Ingress"
* Test Object has key "spec§policyTypes§1" with value "Egress"


___

* Clean the test execution folder