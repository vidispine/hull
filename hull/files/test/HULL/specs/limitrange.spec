# LimitRange

Test creation of objects and features.

* Prepare default test case for kind "LimitRange"

## Render and Validate
* Lint and Render
* Expected number of "22" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Data

* Lint and Render

* Set test object to "release-name-hull-test-cpu"

* Test Object has key "spec§limits§0§max§cpu" with value "800m"
* Test Object has key "spec§limits§0§min§cpu" with value "200m"
* Test Object has key "spec§limits§0§type" with value "Container"

* Set test object to "release-name-hull-test-memory"

* Test Object has key "spec§limits§0§default§memory" with value "512Mi"
* Test Object has key "spec§limits§0§defaultRequest§memory" with value "256Mi"
* Test Object has key "spec§limits§0§type" with value "Container"


* Set test object to "release-name-hull-test-storage"

* Test Object has key "spec§limits§0§max§storage" with value "2Gi"
* Test Object has key "spec§limits§0§min§storage" with value "1Gi"
* Test Object has key "spec§limits§0§type" with value "PersistentVolumeClaim"

___

* Clean the test execution folder