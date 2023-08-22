# Job

Test creation of objects and features.

* Prepare default test case for kind "Job" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "35" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Pod
* Lint and Render
* Check pod functionality

## Selector
* Lint and Render
* Set test object to "release-name-hull-test-no-selector-provided"
* Test Object does not have key "spec§selector"

* Set test object to "release-name-hull-test-selector-provided"
* Test Object has key "spec§selector§matchLabels§test_label" with value "test_value"

## Mixed Transformation Problem
* Lint and Render
* Set test object to "release-name-hull-test-mixed-key-transformations"
* Test Object has key "spec§template§spec§containers§0§volumeMounts" with array value that has "2" items
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§name" with value "custom-installation-files"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§1§name" with value "installation"

* Test Object has key "spec§template§spec§volumes" with array value that has "2" items
* Test Object has key "spec§template§spec§volumes§0§name" with value "custom-installation-files"
* Test Object has key "spec§template§spec§volumes§1§name" with value "installation"

## Certificates
* Prepare default test case for this kind including suites "pod,customcacertificates"
* Render

* Set test object to "release-name-hull-test-mixed-key-transformations"

* Test Object has key "spec§template§spec§containers§0§volumeMounts" with array value that has "5" items
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§name" with value "certs"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§mountPath" with value "/usr/local/share/ca-certificates/custom-ca-certificates-test_cert_1"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§1§name" with value "certs"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§1§mountPath" with value "/usr/local/share/ca-certificates/custom-ca-certificates-test_cert_2"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§2§name" with value "custom-installation-files"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§2§mountPath" with value "/custom-installation-files"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§3§name" with value "etcssl"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§3§mountPath" with value "/etc/ssl/certs"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§4§name" with value "installation"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§4§mountPath" with value "/script"

* Test Object has key "spec§template§spec§volumes" with array value that has "4" items
* Test Object has key "spec§template§spec§volumes§0§name" with value "certs"
* Test Object has key "spec§template§spec§volumes§1§name" with value "custom-installation-files"
* Test Object has key "spec§template§spec§volumes§2§name" with value "etcssl"
* Test Object has key "spec§template§spec§volumes§3§name" with value "installation"

___


* Clean the test execution folder