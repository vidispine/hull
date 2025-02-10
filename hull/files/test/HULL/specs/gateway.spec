# Gateway

Test creation of objects and features.

* Prepare default test case for kind "Gateway"

## Render and Validate

* Lint and Render
* Expected number of "16" objects were rendered on top of basic objects count

## Metadata

* Check basic metadata functionality

## Dynamic Properties

* Lint and Render
* Set test object to "release-name-hull-test-simple"
* Test Object has key "spec§listeners" with array value that has "1" items
* Test Object has key "spec§listeners§0§name" with value "name"
* Test Object has key "spec§listeners§0§port" with integer value "123"
* Test Object has key "spec§listeners§0§protocol" with value "protocol"

* Set test object to "release-name-hull-test-dictionary"
* Test Object has key "spec§listeners" with array value that has "1" items
* Test Object has key "spec§listeners§0§name" with value "name"
* Test Object has key "spec§listeners§0§port" with integer value "123"
* Test Object has key "spec§listeners§0§protocol" with value "protocol"

## Full Example
* Lint and Render
* Set test object to "release-name-hull-test-full-example"

* Test Object has key "spec§addresses" with array value that has "2" items
* Test Object has key "spec§addresses§0§type" with value "IPAddress"
* Test Object has key "spec§addresses§0§value" with value "some hostname"
* Test Object has key "spec§addresses§1§type" with value "IPAddress"
* Test Object has key "spec§addresses§1§value" with value "source hostname"

* Test Object has key "spec§backendTLS§clientCertificateRef§name" with value "onename"
* Test Object has key "spec§backendTLS§clientCertificateRef§group" with value "onegroup"
* Test Object has key "spec§backendTLS§clientCertificateRef§kind" with value "onekind"
* Test Object has key "spec§backendTLS§clientCertificateRef§namespace" with value "onenamespace"

* Test Object has key "spec§gatewayClassName" with value "the-gateway-class"

* Test Object has key "spec§infrastructure§labels§label-a" with value "labelvalue-a"
* Test Object has key "spec§infrastructure§labels§label-source" with value "labelvalue-source"
* Test Object has key "spec§infrastructure§annotations§annotation-a" with value "annotation-a"
* Test Object has key "spec§infrastructure§annotations§annotation-source" with value "annotation-source"
* Test Object has key "spec§infrastructure§parametersRef§name" with value "twoname"
* Test Object has key "spec§infrastructure§parametersRef§kind" with value "twokind"
* Test Object has key "spec§infrastructure§parametersRef§group" with value "twogroup"

* Test Object has key "spec§listeners" with array value that has "2" items

* Test Object has key "spec§listeners§0§name" with value "first-listener"
* Test Object has key "spec§listeners§0§hostname" with value "*.example.com"
* Test Object has key "spec§listeners§0§port" with integer value "123"
* Test Object has key "spec§listeners§0§protocol" with value "protocol"
* Test Object has key "spec§listeners§0§tls§mode" with value "Passthrough"
* Test Object has key "spec§listeners§0§tls§certificateRefs" with array value that has "2" items
* Test Object has key "spec§listeners§0§tls§certificateRefs§0§name" with value "onenamecert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§0§group" with value "onegroupcert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§0§kind" with value "onekindcert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§0§namespace" with value "onenamespace"
* Test Object has key "spec§listeners§0§tls§certificateRefs§1§name" with value "sourcenamecert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§1§group" with value "sourcegroupcert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§1§kind" with value "sourcekindcert"
* Test Object has key "spec§listeners§0§tls§certificateRefs§1§namespace" with value "sourcenamespace"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs" with array value that has "3" items
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§0§name" with value "onenamecacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§0§group" with value "onegroupcacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§0§kind" with value "onekindcacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§0§namespace" with value "onecanamespace"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§1§name" with value "onenamecacert2"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§1§group" with value "onegroupcacert2"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§1§kind" with value "onekindcacert2"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§1§namespace" with value "onecanamespace2"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§2§name" with value "sourcenamecacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§2§group" with value "sourcegroupcacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§2§kind" with value "sourcekindcacert"
* Test Object has key "spec§listeners§0§tls§frontendValidation§caCertificateRefs§2§namespace" with value "sourcecanamespace"
* Test Object has key "spec§listeners§0§tls§options§option-11" with value "opt11"
* Test Object has key "spec§listeners§0§tls§options§option-22" with value "opt22"
* Test Object has key "spec§listeners§0§tls§options§option-source" with value "optsource"
* Test Object has key "spec§listeners§0§allowedRoutes§namespaces§from" with value "All"
* Test Object has key "spec§listeners§0§allowedRoutes§namespaces§selector§matchLabels§labelmatch1" with value "match1"
* Test Object has key "spec§listeners§0§allowedRoutes§namespaces§selector§matchLabels§labelmatch2" with value "match2"
* Test Object has key "spec§listeners§0§allowedRoutes§kinds" with array value that has "1" items
* Test Object has key "spec§listeners§0§allowedRoutes§kinds§0§group" with value "networking.k8s.io"
* Test Object has key "spec§listeners§0§allowedRoutes§kinds§0§kind" with value "Service"

* Test Object has key "spec§listeners§1§name" with value "source-listener"
* Test Object has key "spec§listeners§1§hostname" with value "*.source.com"
* Test Object has key "spec§listeners§1§port" with integer value "123456"
* Test Object has key "spec§listeners§1§protocol" with value "protocol"
* Test Object has key "spec§listeners§1§tls§mode" with value "Passthrough"
* Test Object has key "spec§listeners§1§tls§certificateRefs" with array value that has "1" items
* Test Object has key "spec§listeners§1§tls§certificateRefs§0§name" with value "sourcenamecert"
* Test Object has key "spec§listeners§1§tls§certificateRefs§0§group" with value "sourcegroupcert"
* Test Object has key "spec§listeners§1§tls§certificateRefs§0§kind" with value "sourcekindcert"
* Test Object has key "spec§listeners§1§tls§certificateRefs§0§namespace" with value "sourcenamespace"
* Test Object has key "spec§listeners§1§tls§frontendValidation§caCertificateRefs" with array value that has "1" items
* Test Object has key "spec§listeners§1§tls§frontendValidation§caCertificateRefs§0§name" with value "sourcenamecacert"
* Test Object has key "spec§listeners§1§tls§frontendValidation§caCertificateRefs§0§group" with value "sourcegroupcacert"
* Test Object has key "spec§listeners§1§tls§frontendValidation§caCertificateRefs§0§kind" with value "sourcekindcacert"
* Test Object has key "spec§listeners§1§tls§frontendValidation§caCertificateRefs§0§namespace" with value "sourcecanamespace"
* Test Object has key "spec§listeners§1§tls§options§option-source" with value "optsource"


___

* Clean the test execution folder