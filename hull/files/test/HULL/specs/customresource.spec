# CustomResource

Test creation of objects and features.

* Prepare default test case for kind "CustomResource"

## Render and Validate
* Lint and Render
* Expected number of "17" objects of kind "Dummy" were rendered
* Expected number of "1" objects of kind "MailSender" were rendered
* Expected number of "1" objects of kind "MailReceiver" were rendered
* Expected number of "2" objects of kind "Integration" were rendered
* Expected number of "2" objects of kind "Kustomization" were rendered


## Metadata

Maybe TODO: Check basic metadata functionality

* Lint and Render

## Properties

* Lint and Render

* Set test object to "release-name-hull-test-mail-sender" of kind "MailSender"
* Test Object has key "spec§outgoingAddress" with value "somemailaddress@mail.com"
* Test Object has key "apiVersion" with value "mailSenderApi/v1"
* Test Object has key "kind" with value "MailSender"

* Set test object to "release-name-hull-test-mail-receiver" of kind "MailReceiver"
* Test Object has key "spec§incomingAddress" with value "othermailaddress@mail.com"
* Test Object has key "apiVersion" with value "mailReceiverApi/v1"
* Test Object has key "kind" with value "MailReceiver"

## Load from file

* Lint and Render

* Set test object to "release-name-hull-test-dbzm-kamel-issue-311" of kind "Integration"
* Test Object has key "spec§sources§0§name" with value "dbzm-simple.yaml"
* Test Object has key "spec§sources§0§language" with value "java"
* Test Object has key "spec§sources§0§content" with value of key "code-java-simple.java" from expected.yaml
* Test Object has key "spec§sources§1§name" with value "dbzm-medium.yaml"
* Test Object has key "spec§sources§1§language" with value "java"
* Test Object has key "spec§sources§1§content" with value of key "code-java-medium.java" from expected.yaml
* Test Object has key "spec§sources§2§name" with value "dbzm-complex.yaml"
* Test Object has key "spec§sources§2§language" with value "yaml"
* Test Object has key "spec§sources§2§content" with value of key "code-java-complex.java" from expected.yaml

## Serialize tpl inline

* Lint and Render

* Set test object to "release-name-hull-test-issue-339" of kind "Integration"
* Test Object has key "spec§forProvider§inlinePolicy§0§name" with value "plain-json-string"
* Test Object has key "spec§forProvider§inlinePolicy§0§policy" with value of key "plain-json-string" from expected.yaml
* Test Object has key "spec§forProvider§inlinePolicy§1§name" with value "interpreted-as-flow-style-yaml"
* Test Object has key "spec§forProvider§inlinePolicy§1§policy§Statement§0§Action" with value "ssm:GetParameter*"
* Test Object has key "spec§forProvider§inlinePolicy§1§policy§Statement§0§Effect" with value "Allow"
* Test Object has key "spec§forProvider§inlinePolicy§1§policy§Statement§0§Resource" with value "*"
* Test Object has key "spec§forProvider§inlinePolicy§2§name" with value "interpreted-and-serialized-flow-style-yaml"
* Test Object has key "spec§forProvider§inlinePolicy§2§policy" with value of key "interpreted-and-serialized-flow-style-yaml" from expected.yaml
* Test Object has key "spec§forProvider§inlinePolicy§3§name" with value "interpreted-and-serialized-block-style-yaml"
* Test Object has key "spec§forProvider§inlinePolicy§3§policy" with value of key "interpreted-and-serialized-block-style-yaml" from expected.yaml

## Conditionals

* Lint and Render

* Set test object to "release-name-hull-test-conditionals-true" of kind "Kustomization"
* Test Object has key "spec§decryption§provider" with value "sops"
* Test Object has key "spec§sourceRef§kind" with value "GitRepository"
* Test Object has key "spec§sourceRef§name" with value "flux-system"
* Test Object has key "spec§path.with.dots§prop_a" with value "hello"
* Test Object has key "spec§path.with.dots§prop_b" with value "goodbye"

* Set test object to "release-name-hull-test-conditionals-false" of kind "Kustomization"
* Test Object does not have key "spec§decryption"
* Test Object does not have key "spec§sourceRef"
* Test Object does not have key "spec§path.with.dots"

## Fail
* Fail to render the templates for values file "values.fail-conditionals-reference.hull.yaml" to test execution folder because error contains "Element broken in path hull.config.specific.kustomization.broken was not found"
* Fail to render the templates for values file "values.fail-conditionals-reference.hull.yaml" to test execution folder because error contains "Element encryption_not_exists in path hull.config.specific.kustomization.encryption_not_exists was not found"


___

* Clean the test execution folder