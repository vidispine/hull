# CustomResource

Test creation of objects and features.

* Prepare default test case for kind "CustomResource"

## Render and Validate
* Lint and Render
* Expected number of "17" objects of kind "Dummy" were rendered
* Expected number of "1" objects of kind "MailSender" were rendered
* Expected number of "1" objects of kind "MailReceiver" were rendered


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


___

* Clean the test execution folder