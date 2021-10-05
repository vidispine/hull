# CronJob

Test creation of objects and features.

* Prepare default test case for kind "CronJob"

## Render and Validate
* Render
* Expected number of "3" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Secrets and ConfigMaps and CronJobs
* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-git-gc"
* Test Object has key "spec§schedule" with value "0 0 * * *"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§image" with value "docker.io/alpine/git:v2.26.2"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§value" with value "the_repo"

## Secrets and ConfigMaps and CronJobs - ConfigMap
* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-application_configmap" of kind "ConfigMap"
* Test Object has key "data§dbAdminUsername" with value "the_user"
* Test Object has key "data§dbAdminPassword" with value ""
* Test Object has key "data§gitRepositoryPath" with value "the_repo"

## Secrets and ConfigMaps and CronJobs - Secrets

* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-application_secret" of kind "Secret"
* Test Object has key "data§dbAdminUsername" with Base64 encoded value of "the_user"
* Test Object has key "data§dbAdminPassword" with Base64 encoded value of ""
* Test Object has key "data§gitRepositoryPath" with Base64 encoded value of "the_repo"

___

* Clean the test execution folder