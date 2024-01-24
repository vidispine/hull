# CronJob

Test creation of objects and features.

* Prepare default test case for kind "CronJob"

## Render and Validate
* Lint and Render
* Expected number of "18" objects were rendered
* Validate

## Metadata
* Check basic metadata functionality

## Secrets and ConfigMaps and CronJobs
* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Lint and Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-git-gc"
* Test Object has key "spec§schedule" with value "0 0 * * *"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§image" with value "docker.io/alpine/git:v2.26.2"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§value" with value "the_repo"
* Test Object does not have key "spec§jobTemplate§spec§template§spec§selector"

## Secrets and ConfigMaps and CronJobs - ConfigMap
* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Lint and Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-application-configmap" of kind "ConfigMap"
* Test Object has key "data§dbAdminUsername" with value "the_user"
* Test Object has key "data§dbAdminPassword" with value ""
* Test Object has key "data§gitRepositoryPath" with value "the_repo"

## Secrets and ConfigMaps and CronJobs - Secrets

* Prepare default test case for this kind with test chart "hull-test" and values file "values_cronjob_secret_configmap.hull.yaml" including suites "basic"
* Lint and Render values file "values_cronjob_secret_configmap.hull.yaml"

* Set test object to "release-name-hull-test-application-secret" of kind "Secret"
* Test Object has key "data§dbAdminUsername" with Base64 encoded value of "the_user"
* Test Object has key "data§dbAdminPassword" with Base64 encoded value of ""
* Test Object has key "data§gitRepositoryPath" with Base64 encoded value of "the_repo"


## Applying Defaults
* Prepare default test case for this kind with test chart "hull-test" and values file "values_object_defaults_merging.hull.yaml" including suites ""
* Lint and Render values file "values_object_defaults_merging.hull.yaml"

* Set test object to "release-name-hull-test-deletion-monitor-data-cleanup"
* Test Object has key "spec§schedule" with value "* * 2 *2 *"
* Test Object has key "spec§concurrencyPolicy" with value "Forbid"
* Test Object has key "spec§suspend" set to false

* Test Object has key "spec§jobTemplate§spec§parallelism" with integer value "3"
* Test Object has key "spec§jobTemplate§spec§backoffLimit" with integer value "2"

* Test Object has key "spec§jobTemplate§spec§template§spec§restartPolicy" with value "Never"

* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§name" with value "DAYS_TO_KEEP"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§value" with value "99"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§name" with value "ELASTICSEARCH_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§2§name" with value "ELASTICSEARCH_URI"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§2§value" with value "https://es.uri.com"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§name" with value "ELASTICSEARCH_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_USERNAME"

* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§0§name" with value "DAYS_TO_KEEP"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§0§value" with value "44"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§1§name" with value "DBHOST"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§1§value" with value "dbhost.com"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§2§name" with value "DBNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§2§valueFrom§secretKeyRef§name" with value "release-name-hull-test-deletion-monitor-data-cleanup"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§2§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_DATABASE_NAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§3§name" with value "DBPASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§3§valueFrom§secretKeyRef§name" with value "release-name-hull-test-deletion-monitor-data-cleanup"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§3§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_DATABASE_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§4§name" with value "DBPORT"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§4§value" with value "1453"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§5§name" with value "DBTYPE"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§5§value" with value "mssql"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§6§name" with value "DBUSER"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§6§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_DATABASE_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§6§valueFrom§secretKeyRef§name" with value "release-name-hull-test-deletion-monitor-data-cleanup"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§7§name" with value "DBUSERPOSTFIX"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§7§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_DATABASE_USERNAMESPOSTFIX"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§7§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§8§name" with value "ELASTICSEARCH_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§8§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§8§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§9§name" with value "ELASTICSEARCH_URI"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§9§value" with value "https://es.uri.com"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§10§name" with value "ELASTICSEARCH_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§10§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§10§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§10§name" with value "ELASTICSEARCH_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§env§10§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"

* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§limits§cpu" with value "200m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§limits§memory" with value "256Mi"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§requests§cpu" with value "400m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§requests§memory" with value "456Mi"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§resources§limits§cpu" with value "200m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§resources§limits§memory" with value "256Mi"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§resources§requests§cpu" with value "400m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§resources§requests§memory" with value "456Mi"

* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§volumeMounts§0§name" with value "configmap"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§volumeMounts§0§mountPath" with value "/scripts"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§volumeMounts§1§name" with value "etcssl"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§volumeMounts§1§mountPath" with value "/etc/ssl/certs"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§volumeMounts§0§name" with value "other_configmap"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§volumeMounts§0§mountPath" with value "/other/configmap"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§volumeMounts§1§name" with value "etcssl"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§1§volumeMounts§1§mountPath" with value "/etc/ssl/certs"

* Set test object to "release-name-hull-test-sources-test"

* Test Object has key "spec§schedule" with value "* * 2 3 *"
* Test Object has key "spec§concurrencyPolicy" with value "TestOverwrite"
* Test Object has key "spec§jobTemplate§spec§backoffLimit" with integer value "20"
* Test Object has key "spec§jobTemplate§spec§template§spec§restartPolicy" with value "NeverEver"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§name" with value "DAYS_TO_KEEP"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§0§value" with value "999"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§name" with value "ELASTICSEARCH_PASSWORD"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§1§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_PASSWORD_NEW"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§2§name" with value "ELASTICSEARCH_URI"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§2§value" with value "https://es.uri.com/changed"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§name" with value "ELASTICSEARCH_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§valueFrom§secretKeyRef§name" with value "release-name-hull-test-auth"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§3§valueFrom§secretKeyRef§key" with value "AUTH_BASIC_INDEX_USERNAME"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§4§name" with value "ELASTICSEARCH_ZZZ"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§env§4§value" with value "ZZZ"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§limits§cpu" with value "9m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§limits§memory" with value "9Mi"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§requests§cpu" with value "99m"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§resources§requests§memory" with value "99Mi"


___

* Clean the test execution folder