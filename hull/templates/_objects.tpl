{{- /*
############################################ OBJECT OVERRIDES ##############################################
*/ -}}



{{- /*
### none - nothing special to apply
*/ -}}
{{ define "this.none" }}
{{- end -}}



{{- /*
### emptynamespace - Sets an empty namespace
*/ -}}
{{ define "this.emptynamespace" }}
metadata:
  namespace: ""
{{- end -}}



{{- /*
################################################# PREPARE ALL #####################################################
*/ -}}



{{ define "hull.objects.prepare.all" }}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $rootContext := (index . "ROOT_CONTEXT") -}}
{{- /*
### Load all handled object types step by step for better visibility
*/ -}}
{{- $allObjects := dict -}}



{{- /*
### Load plain objects
*/ -}}
{{- $template := "hull.object.base.plain" }}
{{- $allObjects = merge $allObjects (dict "Namespace" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "ServiceAccount" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "StorageClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "storage.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "CustomResource" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "PriorityClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "scheduling.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "Endpoints" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "EndpointSlice" (dict "HULL_TEMPLATE" $template "API_VERSION" "discovery.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "MutatingWebhookConfiguration" (dict "HULL_TEMPLATE" $template "API_VERSION" "admissionregistration.k8s.io/v1" "DYNAMIC_FIELDS" (dict "webhooks" "hull.object.base.webhook.webhooks"))) }}
{{- $allObjects = merge $allObjects (dict "ValidatingWebhookConfiguration" (dict "HULL_TEMPLATE" $template "API_VERSION" "admissionregistration.k8s.io/v1" "DYNAMIC_FIELDS" (dict "webhooks" "hull.object.base.webhook.webhooks"))) }}

{{- /*
### Load pod based objects
*/ -}}
{{- $template = "hull.object.base.pod" }}
{{- $allObjects = merge $allObjects (dict "Deployment" (dict "HULL_TEMPLATE" $template "API_VERSION" "apps/v1")) }}
{{- $allObjects = merge $allObjects (dict "DaemonSet" (dict "HULL_TEMPLATE" $template "API_VERSION" "apps/v1")) }}
{{- $allObjects = merge $allObjects (dict "Job" (dict "HULL_TEMPLATE" $template "API_VERSION" "batch/v1" "NO_SELECTOR" true)) }}
{{- $allObjects = merge $allObjects (dict "StatefulSet" (dict "HULL_TEMPLATE" $template "API_VERSION" "apps/v1")) }}

{{- /*
### Load spec based objects
*/ -}}
{{- $template = "hull.object.base.spec" }}
{{- $allObjects = merge $allObjects (dict "PersistentVolume" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "PersistentVolumeClaim" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "ServiceMonitor" (dict "HULL_TEMPLATE" $template "API_VERSION" "monitoring.coreos.com/v1")) }}
{{- $allObjects = merge $allObjects (dict "PodDisruptionBudget" (dict "HULL_TEMPLATE" $template "API_VERSION" "policy/v1")) }}
{{- $allObjects = merge $allObjects (dict "ResourceQuota" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "NetworkPolicy" (dict "HULL_TEMPLATE" $template "API_VERSION" "networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "IngressClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "LimitRange" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "HorizontalPodAutoscaler" (dict "API_VERSION" "autoscaling/v2" "DYNAMIC_FIELDS" (dict "scaleTargetRef" "hull.object.horizontalpodautoscaler.scaleTargetRef"))) }}
{{- $allObjects = merge $allObjects (dict "BackendLBPolicy" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1alpha2" "DYNAMIC_FIELDS" (dict "targetRefs" "hull.object.base.dynamic.simple.array"))) }}
{{- $allObjects = merge $allObjects (dict "BackendTLSPolicy" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1alpha3" "DYNAMIC_FIELDS" (dict "targetRefs" "hull.object.base.dynamic.simple.array"))) }}
{{- $allObjects = merge $allObjects (dict "GatewayClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "Gateway" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1" "DYNAMIC_FIELDS" (dict "addresses" "hull.object.base.dynamic.simple.array" "listeners" "hull.object.base.gateway.api.gateway.listener"))) }}
{{- $allObjects = merge $allObjects (dict "GRPCRoute" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1" "DYNAMIC_FIELDS" (dict "parentRefs" "hull.object.base.dynamic.simple.array" "rules" "hull.object.base.gateway.api.extended.route.rules"))) }}
{{- $allObjects = merge $allObjects (dict "ReferenceGrant" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1beta1" "DYNAMIC_FIELDS" (dict "from" "hull.object.base.dynamic.simple.array" "to" "hull.object.base.dynamic.simple.array"))) }}
{{- $allObjects = merge $allObjects (dict "TCPRoute" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1alpha2" "DYNAMIC_FIELDS" (dict "parentRefs" "hull.object.base.dynamic.simple.array" "rules" "hull.object.base.gateway.api.simple.route.rules"))) }}
{{- $allObjects = merge $allObjects (dict "TLSRoute" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1alpha2" "DYNAMIC_FIELDS" (dict "parentRefs" "hull.object.base.dynamic.simple.array" "rules" "hull.object.base.gateway.api.simple.route.rules"))) }}
{{- $allObjects = merge $allObjects (dict "UDPRoute" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1alpha2" "DYNAMIC_FIELDS" (dict "parentRefs" "hull.object.base.dynamic.simple.array" "rules" "hull.object.base.gateway.api.simple.route.rules"))) }}
{{- $allObjects = merge $allObjects (dict "HTTPRoute" (dict "HULL_TEMPLATE" $template "API_VERSION" "gateway.networking.k8s.io/v1" "DYNAMIC_FIELDS" (dict "parentRefs" "hull.object.base.dynamic.simple.array" "rules" "hull.object.base.gateway.api.extended.route.rules"))) }}

{{- /*
### Load rbac'ed objects
*/ -}}
{{- $template = "hull.object.base.rbac" }}
{{- $allObjects = merge $allObjects (dict "RoleBinding" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "ClusterRoleBinding" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1" "PARENT_TEMPLATE" "this.emptynamespace")) }}
{{- $allObjects = merge $allObjects (dict "Role" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1" "DYNAMIC_FIELDS" (dict "rules" "hull.object.base.role.rules"))) }}
{{- $allObjects = merge $allObjects (dict "ClusterRole" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1" "PARENT_TEMPLATE" "this.emptynamespace" "DYNAMIC_FIELDS" (dict "rules" "hull.object.base.role.rules"))) }}
{{- /*

{{- /*
### Load custom objects
*/ -}}
{{- $allObjects = merge $allObjects (dict "ConfigMap" (dict))  }}
{{- $allObjects = merge $allObjects (dict "Secret" (dict)) }}
{{- $allObjects = merge $allObjects (dict "Registry" (dict "API_KIND" "Secret")) }}
{{- $allObjects = merge $allObjects (dict "Service" (dict)) }}
{{- $allObjects = merge $allObjects (dict "Ingress" (dict "API_VERSION" "networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "CronJob" (dict "API_VERSION" "batch/v1")) }}
{{- $temp := set . "HULL_OBJECTS" $allObjects }}
{{- include "hull.objects.render" . }}
{{- end -}}



{{- /*
################################################# RENDER #####################################################
*/ -}}
{{- define "hull.objects.render" -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $rootContext := (index . "ROOT_CONTEXT") -}}
{{- $allObjects := (index . "HULL_OBJECTS") -}}
{{- $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $rootContext "SOURCE" $rootContext.Values.hull "HULL_ROOT_KEY" $hullRootKey "SOURCE_PATH" (list "hull")) | fromYaml }}
{{- if gt ((index $rootContext.Values $hullRootKey).config.general.render.passes | int) 1 -}}
{{- range $i, $e := untilStep 1 ((index $rootContext.Values $hullRootKey).config.general.render.passes | int) 1 -}}
{{- $rendered = include "hull.util.transformation" (dict "PARENT_CONTEXT" $rootContext "SOURCE" $rootContext.Values.hull "HULL_ROOT_KEY" $hullRootKey "SOURCE_PATH" (list "hull")) | fromYaml }}
{{- end -}}
{{- end -}}
{{- $errorMessages := "" }}
{{- range $objectType, $objectTypeSpec := $allObjects }}
{{- $lowerObjectType := $objectType | lower }}
{{- $apiKind := $objectType }}
{{- if (hasKey $objectTypeSpec "API_KIND") }}
{{- $apiKind = $objectTypeSpec.API_KIND }}
{{- end }}
{{- $apiVersion := "v1" }}
{{- if (hasKey $objectTypeSpec "API_VERSION") }}
{{- $apiVersion = $objectTypeSpec.API_VERSION }}
{{- end }}
{{- $enabledDefault := (index (index $rootContext.Values $hullRootKey).objects $lowerObjectType)._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- $hullTemplate := "" }}
{{- if (hasKey $objectTypeSpec "HULL_TEMPLATE") }}
{{- $hullTemplate = $objectTypeSpec.HULL_TEMPLATE }}
{{- else }}
{{- $hullTemplate = printf "hull.object.%s" $lowerObjectType }}
{{- end }}
{{- $parentTemplate := "" }}
{{- if (hasKey $objectTypeSpec "PARENT_TEMPLATE") }}
{{- $parentTemplate = $objectTypeSpec.PARENT_TEMPLATE }}
{{- else }}
{{- $parentTemplate = "this.none" }}
{{- end }}
{{- $noSelector := false }}
{{- if (hasKey $objectTypeSpec "NO_SELECTOR") }}
{{- $noSelector = $objectTypeSpec.NO_SELECTOR }}
{{- end }}
{{- $dynamicFields := default dict (index $objectTypeSpec "DYNAMIC_FIELDS") -}}

{{- range $objectKey, $spec := (index (index $rootContext.Values $hullRootKey).objects $lowerObjectType) }}
{{- /*
### Get the default spec with key _HULL_OBJECT_TYPE_DEFAULT_ for the object to be merged with all instances
*/ -}}

{{- if (or (ne $objectKey "_HULL_OBJECT_TYPE_DEFAULT_")) -}}
{{- if (or (gt (len (keys (default dict $spec))) 0) (not (kindIs "invalid" $spec))) -}}
{{- $defaultSpec := fromYaml (include "hull.objects.defaults" (dict "PARENT_CONTEXT" $rootContext "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType) ) -}}
{{- $enabledDefault = dig "enabled" true $defaultSpec -}}
{{- $specDisabled := and (hasKey $spec "enabled") (not $spec.enabled) }}

{{- if (and (not $specDisabled) (or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault))) -}}
{{ $spec = merge (omit $spec "sources") $defaultSpec }}

{{- /*
### Now render the result object instance
*/ -}}
{{- $objectSpec := dict }}
{{- $namingElement := $objectKey -}}
{{- if and $spec $spec.metadataNameOverride -}}
{{- $namingElement = $spec.metadataNameOverride -}}
{{- $spec = unset $spec "metadataNameOverride" }}
{{- end -}}
{{- if true -}}
{{- $objectSpec = include "hull.util.merge" (merge (dict "PARENT_CONTEXT" $rootContext "PARENT_TEMPLATE" $parentTemplate "API_VERSION" (default $apiVersion $spec.apiVersion) "API_KIND" (default $apiKind $spec.apiKind) "COMPONENT" $namingElement "SPEC" $spec "DEFAULT_COMPONENT" $defaultSpec "HULL_ROOT_KEY" $hullRootKey "NO_SELECTOR" $noSelector "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectKey "DYNAMIC_FIELDS" $dynamicFields) (dict "LOCAL_TEMPLATE" (printf "%s" $hullTemplate))) | fromYaml }}
{{- if (gt (len (keys (default dict $objectSpec))) 0) -}}
{{- $errorMessage := include "hull.util.error.check" (dict "OBJECT" $objectSpec "OBJECT_TYPE" $lowerObjectType) -}}
{{- if (and (hasKey $objectSpec "Error") (eq (len (keys ($objectSpec))) 1)) -}}
{{- if (index $rootContext.Values $hullRootKey).config.general.errorChecks.objectYamlValid -}}
{{- $errorMessage = printf "%s [%s %s: %s for %s %s due to YAML error '%s']" $errorMessage "HULL failed with error" "BROKEN-OBJECT-YAML" "A broken object YAML was encountered" $lowerObjectType $objectKey (index $objectSpec "Error") -}}
{{- end -}}
{{- end -}}
{{- if (ne $errorMessage "") -}}
{{ $errorMessages = printf "%s%s" $errorMessages $errorMessage }}


---
{{ else }}
{{- $printedObject := toYaml $objectSpec -}}
{{- range $replacementName, $replacementValue := (index $rootContext.Values $hullRootKey).config.general.postRender.globalStringReplacements -}}
{{- if $replacementValue.enabled -}}
{{- $targetValue := $replacementValue.replacement -}}
{{- $replacementStaticKeys := list "OBJECT_INSTANCE_KEY" "OBJECT_INSTANCE_KEY_RESOLVED" "OBJECT_INSTANCE_NAME" -}}
{{- if has $replacementValue.replacement $replacementStaticKeys  -}}
{{- if eq $replacementValue.replacement "OBJECT_INSTANCE_KEY" -}}
{{- $targetValue = $objectKey -}}
{{- end -}}
{{- if eq $replacementValue.replacement "OBJECT_INSTANCE_KEY_RESOLVED" -}}
{{- $targetValue = $namingElement -}}
{{- end -}}
{{- if eq $replacementValue.replacement "OBJECT_INSTANCE_NAME" -}}
{{- $targetValue = printf "%s" $objectSpec.metadata.name -}}
{{- end -}}
{{- end -}}
{{- $printedObject = $printedObject | replace $replacementValue.string $targetValue -}}
{{- end -}}
{{- end -}}
{{ $printedObject }}


---
{{ end -}}
{{- end -}}
{{- else -}}
{{- /* 
### DEBUG SPEC 
*/ -}}
{{ toYaml $spec }}


---
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- end -}}
{{- if (ne $errorMessages "") -}}
{{- fail $errorMessages -}}
{{- end -}}
{{- end -}}