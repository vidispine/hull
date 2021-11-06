# CustomResource

Test creation of objects and features.

* Prepare default test case for kind "CustomResource"

## Render and Validate
* Render
* Expected number of "6" objects of kind "Dummy" were rendered
* Expected number of "1" objects of kind "MailSender" were rendered
* Expected number of "1" objects of kind "MailReceiver" were rendered


## Metadata

Maybe TODO: Check basic metadata functionality

* Render

## Properties

* Render

* Set test object to "release-name-hull-test-mail_sender" of kind "MailSender"
* Test Object has key "spec§outgoingAddress" with value "somemailaddress@mail.com"
* Test Object has key "apiVersion" with value "mailSenderApi/v1"
* Test Object has key "kind" with value "MailSender"

* Set test object to "release-name-hull-test-mail_receiver" of kind "MailReceiver"
* Test Object has key "spec§incomingAddress" with value "othermailaddress@mail.com"
* Test Object has key "apiVersion" with value "mailReceiverApi/v1"
* Test Object has key "kind" with value "MailReceiver"

___

* Clean the test execution folder