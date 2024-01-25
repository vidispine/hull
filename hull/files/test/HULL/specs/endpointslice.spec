# EndpointSlice

Test creation of objects and features.

* Prepare default test case for kind "EndpointSlice"

## Render and Validate
* Lint and Render
* Expected number of "21" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## References

* Lint and Render

* Set test object to "release-name-hull-test-test-one"
* Test Object has key "addressType" with value "FQDN"
* Test Object has key "endpoints§0§addresses§0" with value "a.b.com"
* Test Object has key "endpoints§0§addresses§1" with value "b.b.com"
* Test Object has key "endpoints§0§addresses§2" with value "c.b.com"
* Test Object has key "endpoints§0§conditions§ready" set to true
* Test Object has key "endpoints§0§conditions§serving" set to true
* Test Object has key "endpoints§0§conditions§terminating" set to true
* Test Object has key "endpoints§0§hints§forZones§0§name" with value "zone1"
* Test Object has key "endpoints§0§hints§forZones§1§name" with value "zone2"
* Test Object has key "endpoints§0§hints§forZones§2§name" with value "zone3"
* Test Object has key "endpoints§0§hostname" with value "some_host"
* Test Object has key "endpoints§0§nodeName" with value "some_node"
* Test Object has key "endpoints§0§targetRef§kind" with value "Service"
* Test Object has key "endpoints§0§targetRef§apiVersion" with value "v1"
* Test Object has key "endpoints§0§targetRef§name" with value "a_service"
* Test Object has key "endpoints§0§targetRef§namespace" with value "some_namespace"
* Test Object has key "endpoints§0§zone" with value "some_zone"
* Test Object has key "endpoints§1§addresses§0" with value "a.c.com"
* Test Object has key "endpoints§1§addresses§1" with value "b.c.com"
* Test Object has key "endpoints§1§addresses§2" with value "c.c.com"
* Test Object has key "endpoints§1§conditions§ready" set to false
* Test Object has key "endpoints§1§conditions§serving" set to false
* Test Object has key "endpoints§1§conditions§terminating" set to false
* Test Object has key "endpoints§1§hints§forZones§0§name" with value "zone4"
* Test Object has key "endpoints§1§hints§forZones§1§name" with value "zone5"
* Test Object has key "endpoints§1§hints§forZones§2§name" with value "zone6"
* Test Object has key "endpoints§1§hostname" with value "other_host"
* Test Object has key "endpoints§1§nodeName" with value "other_node"
* Test Object has key "endpoints§1§targetRef§kind" with value "Service"
* Test Object has key "endpoints§1§targetRef§apiVersion" with value "v1"
* Test Object has key "endpoints§1§targetRef§name" with value "b_service"
* Test Object has key "endpoints§1§targetRef§namespace" with value "other_namespace"
* Test Object has key "endpoints§1§zone" with value "other_zone"
* Test Object has key "ports§0§appProtocol" with value "HTTP"
* Test Object has key "ports§0§name" with value "test_tcp"
* Test Object has key "ports§0§protocol" with value "TCP"
* Test Object has key "ports§0§port" with integer value "87"
* Test Object has key "ports§1§appProtocol" with value "HTTP2"
* Test Object has key "ports§1§name" with value "test_udp"
* Test Object has key "ports§1§protocol" with value "UDP"
* Test Object has key "ports§1§port" with integer value "88"