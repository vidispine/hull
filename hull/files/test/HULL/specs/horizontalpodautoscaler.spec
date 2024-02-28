# HorizontalPodAutoscaler

Test creation of objects and features.

* Prepare default test case for kind "HorizontalPodAutoscaler"

## Render and Validate
* Lint and Render
* Expected number of "22" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## References

* Lint and Render

* Set test object to "release-name-hull-test-internal"
* Test Object has key "spec§minReplicas" with integer value "1"
* Test Object has key "spec§maxReplicas" with integer value "2"
* Test Object has key "spec§scaleTargetRef§apiVersion" with value "v1"
* Test Object has key "spec§scaleTargetRef§kind" with value "Deployment"
* Test Object has key "spec§scaleTargetRef§name" with value "release-name-hull-test-target_deployment"
* Test Object has key "spec§behavior§scaleUp§selectPolicy" with value "select_policy_up"
* Test Object has key "spec§behavior§scaleUp§stabilizationWindowSeconds" with integer value "999"
* Test Object has key "spec§behavior§scaleDown§selectPolicy" with value "select_policy_down"
* Test Object has key "spec§behavior§scaleDown§stabilizationWindowSeconds" with integer value "111"

* Set test object to "release-name-hull-test-external"
* Test Object has key "spec§minReplicas" with integer value "1"
* Test Object has key "spec§maxReplicas" with integer value "2"
* Test Object has key "spec§scaleTargetRef§apiVersion" with value "v1"
* Test Object has key "spec§scaleTargetRef§kind" with value "Deployment"
* Test Object has key "spec§scaleTargetRef§name" with value "target_deployment"
* Test Object has key "spec§behavior§scaleUp§selectPolicy" with value "select_policy_up"
* Test Object has key "spec§behavior§scaleUp§stabilizationWindowSeconds" with integer value "999"
* Test Object has key "spec§behavior§scaleDown§selectPolicy" with value "select_policy_down"
* Test Object has key "spec§behavior§scaleDown§stabilizationWindowSeconds" with integer value "111"


