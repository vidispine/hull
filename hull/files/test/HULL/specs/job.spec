# Job

Test creation of objects and features.

* Prepare default test case for kind "Job" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "44" objects were rendered on top of basic objects count
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

## Render Hull Job to ConfigMap
* Lint and Render
* Set test object to "release-name-hull-test-source-enabled-disabled"

* Test Object has key "metadata§annotations§annotation" with value "I am an Annotation"
* Test Object has key "metadata§labels§job-type" with value "videoengine-mediaframework"
* Test Object has key "spec§template§metadata§annotations§annotation" with value "I am an Annotation"
* Test Object has key "spec§template§metadata§labels§job-type" with value "videoengine-mediaframework"
* Test Object has key "spec§backoffLimit" with integer value "0"
* Test Object has key "spec§ttlSecondsAfterFinished" with integer value "300"
* Test Object has key "spec§template§spec§containers§0§env§0§name" with value "TRANSCODER_LOG_LEVEL"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "INFO"
* Test Object has key "spec§template§spec§containers§0§image" with value "videoengine/transcoders4m:24.1.20"
* Test Object has key "spec§template§spec§containers§0§name" with value "transcoder"
* Test Object has key "spec§template§spec§containers§0§restartPolicy" with value "Never"
* Test Object has key "spec§template§spec§imagePullSecrets§0§name" with value "release-name-hull-test-example-registry"
* Test Object has key "spec§template§spec§imagePullSecrets§1§name" with value "release-name-hull-test-local-registry"
* Test Object has key "spec§template§spec§serviceAccountName" with value "release-name-hull-test-mediaframework-transcode"
* Test Object has key "spec§ttlSecondsAfterFinished" with integer value "300"

* Set test object to "release-name-hull-test-test-force-enable-on" of kind "ConfigMap"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "metadata§annotations§annotation" with value "I am an Annotation"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "metadata§labels§job-type" with value "videoengine-mediaframework"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§metadata§annotations§annotation" with value "I am an Annotation"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§metadata§labels§job-type" with value "videoengine-mediaframework"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§backoffLimit" with integer value "0"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§ttlSecondsAfterFinished" with integer value "300"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§containers§0§env§0§name" with value "TRANSCODER_LOG_LEVEL"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§containers§0§env§0§value" with value "INFO"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§containers§0§image" with value "videoengine/transcoders4m:24.1.20"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§containers§0§name" with value "transcoder"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§containers§0§restartPolicy" with value "Never"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§imagePullSecrets§0§name" with value "release-name-hull-test-example-registry"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§imagePullSecrets§1§name" with value "release-name-hull-test-local-registry"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§template§spec§serviceAccountName" with value "release-name-hull-test-mediaframework-transcode"
* Test Object has key "data§mediaframework-job" containing serialized "YAML" having key "spec§ttlSecondsAfterFinished" with integer value "300"

## Certificates
* Prepare default test case for this kind including suites "pod,customcacertificates"
* Lint and Render

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