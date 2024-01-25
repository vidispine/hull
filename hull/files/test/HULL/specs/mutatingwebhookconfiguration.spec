# MutatingebhookConfiguration

Test creation of objects and features.

* Prepare default test case for kind "MutatingWebhookConfiguration"

## Render and Validate
* Lint and Render
* Expected number of "20" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## References

* Lint and Render

* Set test object to "release-name-hull-test-standard"
* Test Object has key "webhooks§0§failurePolicy" with value "Ignore"
* Test Object has key "webhooks§0§matchPolicy" with value "Exact"
* Test Object has key "webhooks§0§name" with value "my webhook"
* Test Object has key "webhooks§0§clientConfig§service§name" with value "service_check"
* Test Object has key "webhooks§0§clientConfig§service§namespace" with value "service_check_namespace"
* Test Object has key "webhooks§0§reinvocationPolicy" with value "IfNeeded"
* Test Object has key "webhooks§0§sideEffects" with value "None"
* Test Object has key "webhooks§0§admissionReviewVersions§0" with value "first_draft"
* Test Object has key "webhooks§0§timeoutSeconds" with integer value "30"
* Test Object has key "webhooks§1§failurePolicy" with value "Fail"
* Test Object has key "webhooks§1§name" with value "my webhook 2"
* Test Object has key "webhooks§1§clientConfig§url" with value "http://some_url"
* Test Object has key "webhooks§1§reinvocationPolicy" with value "IfNeeded"
* Test Object has key "webhooks§1§sideEffects" with value "NoneOnDryRun"
* Test Object has key "webhooks§1§admissionReviewVersions§0" with value "second_draft"

## Enable Disable Webhook
* Lint and Render
* Set test object to "release-name-hull-test-webhook-enabled-false-true"
* Test Object has key "webhooks" with array value that has "3" items

* Test Object has key "webhooks§0§name" with value "test_enabled"
* Test Object has key "webhooks§1§name" with value "test_enabled_missing"
* Test Object has key "webhooks§2§name" with value "test_enabled_transform"