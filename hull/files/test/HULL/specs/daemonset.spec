# DaemonSet

Test creation of objects and features.

* Prepare default test case for kind "DaemonSet" including suites "pod"

## Render and Validate
* Lint and Render
* Expected number of "49" objects were rendered on top of basic objects count
* Validate

## Metadata
* Check basic metadata functionality

## Pod
* Lint and Render
* Check pod functionality
## Explicit selector
* Prepare test case "daemonset" for kind "DaemonSet" with test chart "hull-test" and values file "values_explicit_selector.hull.yaml"
* Lint and Render values file "values_explicit_selector.hull.yaml"

* Set test object to "release-name-hull-test-explicit-selector"
* Test Object has key "spec§selector§matchLabels" with dictionary value that has "2" items
* Test Object has key "spec§selector§matchLabels§app" with value "explicit"
* Test Object has key "spec§selector§matchLabels§tier" with value "web"
* Test Object has key "spec§template§metadata§labels§app" with value "explicit"
* Test Object has key "spec§template§metadata§labels§tier" with value "web"
* Test Object has key "spec§template§metadata§labels§team" with value "payments"
* Test Object does not have key "spec§template§metadata§labels§app.kubernetes.io/component"
* Test Object has key "metadata§labels§app.kubernetes.io/component" with value "explicit-selector"

___


* Clean the test execution folder