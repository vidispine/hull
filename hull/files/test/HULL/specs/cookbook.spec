# Cookbook

Every recipe of hull/files/doc/cookbook.md is rendered exactly as written and checked for what
its explanation promises.

## Every recipe is tested
* Every recipe of the cookbook is tested

## Web application
* Render the cookbook recipe "web-application"
* Set test object to "release-name-hull-test-web" of kind "Service"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "web"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§template§metadata§labels§app.kubernetes.io/component" with value "web"
* Test Object has key "spec§template§spec§containers§0§image" with value "example/shop-web:2.3.0"
* Set test object to "release-name-hull-test-web" of kind "Ingress"
* Test Object has key "spec§rules§0§host" with value "shop.example.com"
* Test Object has key "spec§rules§0§http§paths§0§backend§service§name" with value "release-name-hull-test-web"
* Test Object has key "spec§tls§0§secretName" with value "release-name-hull-test-web-tls"
* Test Object has key "spec§tls§0§hosts" with array value that has "1" items
* Test Object has key "spec§tls§0§hosts§0" with value "shop.example.com"

## Configuration with automatic restarts
* Render the cookbook recipe "configuration-restart"
* Set test object to "release-name-hull-test-settings" of kind "ConfigMap"
* Test Object has key "data§app.yaml" with value containing "logLevel: info"
* Test Object has key "data§nginx.conf" with value containing "listen 8080;"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§template§metadata§annotations§hashsum.configmap.release-name-hull-test-settings/app.yaml" with value matching regex "^[0-9a-f]{64}$"
* Test Object has key "spec§template§metadata§annotations§hashsum.configmap.release-name-hull-test-settings/nginx.conf" with value matching regex "^[0-9a-f]{64}$"
* Test Object has key "spec§template§spec§volumes§0§configMap§name" with value "release-name-hull-test-settings"

## Settings shared by many containers
* Render the cookbook recipe "shared-container-settings"
* Set test object to "release-name-hull-test-api" of kind "Deployment"
* Test Object has key "spec§template§spec§containers§0§resources§requests§cpu" with value "100m"
* Test Object has key "spec§template§spec§containers§0§resources§requests§memory" with value "128Mi"
* Test Object has key "spec§template§spec§containers§0§securityContext§readOnlyRootFilesystem" set to true
* Set test object to "release-name-hull-test-worker" of kind "Deployment"
* Test Object has key "spec§template§spec§containers§0§resources§requests§cpu" with value "500m"
* Test Object has key "spec§template§spec§containers§0§resources§requests§memory" with value "128Mi"
* Test Object has key "spec§template§spec§containers§0§securityContext§readOnlyRootFilesystem" set to true

## Database migration as Helm hook
* Render the cookbook recipe "migration-hook"
* Set test object to "release-name-hull-test-database" of kind "Secret"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "-1"
* Test Object has key "data§password" with value "Y2hhbmdlLW1l"
* Set test object to "release-name-hull-test-migrate" of kind "Job"
* Test Object has key "metadata§annotations§helm.sh/hook" with value "pre-install,pre-upgrade"
* Test Object has key "metadata§annotations§helm.sh/hook-weight" with value "0"
* Test Object has key "spec§backoffLimit" with integer value "2"
* Test Object has key "spec§template§spec§containers§0§env§0§value" with value "postgres.example.com"
* Test Object has key "spec§template§spec§containers§0§env§1§valueFrom§secretKeyRef§name" with value "release-name-hull-test-database"

## Pinning images by digest
* Render the cookbook recipe "digest-pinning"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§template§spec§containers§0§image" with value "registry.example.com/example/shop-web@sha256:1ff6c18fbef2045af6b9c16bf034cc421a29027b800e4f9b68ae9b1cb3e9ae07"

## Optional components
* Render the cookbook recipe "optional-components"
* Set test object to "release-name-hull-test-search" of kind "Deployment"
* Test object "release-name-hull-test-search" of kind "ServiceMonitor" does not exist

## ServiceAccount with permissions
* Render the cookbook recipe "service-account-rbac"
* Set test object to "release-name-hull-test-app" of kind "ServiceAccount"
* Set test object to "release-name-hull-test-app" of kind "Role"
* Test Object has key "rules§0§resources§0" with value "configmaps"
* Set test object to "release-name-hull-test-app" of kind "RoleBinding"
* Test Object has key "roleRef§name" with value "release-name-hull-test-app"
* Test Object has key "subjects§0§name" with value "release-name-hull-test-app"
* Test Object has key "subjects§0§namespace" with value "default"
* Set test object to "release-name-hull-test-app" of kind "Deployment"
* Test Object has key "spec§template§spec§serviceAccountName" with value "release-name-hull-test-app"

## Database with persistent storage
* Render the cookbook recipe "stateful-database"
* Set test object to "release-name-hull-test-db" of kind "StatefulSet"
* Test Object has key "spec§serviceName" with value "release-name-hull-test-db"
* Test Object has key "spec§volumeClaimTemplates§0§metadata§name" with value "data"
* Test Object has key "spec§template§spec§containers§0§volumeMounts§0§name" with value "data"
* Set test object to "release-name-hull-test-db" of kind "Service"
* Test Object has key "spec§clusterIP" with value "None"
* Test Object has key "spec§selector§app.kubernetes.io/component" with value "db"

## Scheduled job
* Render the cookbook recipe "scheduled-job"
* Set test object to "release-name-hull-test-cleanup" of kind "CronJob"
* Test Object has key "spec§schedule" with value "0 3 * * *"
* Test Object has key "spec§concurrencyPolicy" with value "Forbid"
* Test Object has key "spec§jobTemplate§spec§backoffLimit" with integer value "1"
* Test Object has key "spec§jobTemplate§spec§template§spec§restartPolicy" with value "OnFailure"
* Test Object has key "spec§jobTemplate§spec§template§spec§containers§0§args§1" with value "--older-than=7d"

## Restricting traffic to a workload
* Render the cookbook recipe "network-policy"
* Set test object to "release-name-hull-test-web" of kind "NetworkPolicy"
* Test Object has key "spec§podSelector§matchLabels§app.kubernetes.io/component" with value "web"
* Test Object has key "spec§podSelector§matchLabels§app.kubernetes.io/instance" with value "release-name"
* Test Object has key "spec§podSelector§matchLabels§app.kubernetes.io/name" with value "hull-test"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§selector§matchLabels§app.kubernetes.io/component" with value "web"

## Init containers in a fixed order
* Render the cookbook recipe "init-container-order"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§template§spec§initContainers§0§name" with value "wait-for-database"
* Test Object has key "spec§template§spec§initContainers§1§name" with value "migrate-schema"

## Using objects that are not part of the chart
* Render the cookbook recipe "external-objects"
* Set test object to "release-name-hull-test-web" of kind "Deployment"
* Test Object has key "spec§template§spec§containers§0§envFrom§0§configMapRef§name" with value "platform-settings"
* Test Object has key "spec§template§spec§containers§0§env§0§valueFrom§secretKeyRef§name" with value "shared-api-token"
* Test Object has key "spec§template§spec§volumes§0§secret§secretName" with value "company-ca"
