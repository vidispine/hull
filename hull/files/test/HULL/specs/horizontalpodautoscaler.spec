# HorizontalPodAutoscaler

Test creation of objects and features.

* Prepare default test case for kind "HorizontalPodAutoscaler"

## Render and Validate
* Render
* Expected number of "8" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## References

* Render

* Set test object to "release-name-hull-test-internal"
* Test Object has key "spec§minReplicas" with integer value "1"
* Test Object has key "spec§maxReplicas" with integer value "2"
* Test Object has key "spec§targetCPUUtilizationPercentage" with integer value "50"
* Test Object has key "spec§scaleTargetRef§apiVersion" with value "v1"
* Test Object has key "spec§scaleTargetRef§kind" with value "Deployment"
* Test Object has key "spec§scaleTargetRef§name" with value "release-name-hull-test-target_deployment"

* Set test object to "release-name-hull-test-external"
* Test Object has key "spec§minReplicas" with integer value "1"
* Test Object has key "spec§maxReplicas" with integer value "2"
* Test Object has key "spec§targetCPUUtilizationPercentage" with integer value "50"
* Test Object has key "spec§scaleTargetRef§apiVersion" with value "v1"
* Test Object has key "spec§scaleTargetRef§kind" with value "Deployment"
* Test Object has key "spec§scaleTargetRef§name" with value "target_deployment"

