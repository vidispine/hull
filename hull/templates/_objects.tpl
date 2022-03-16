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
{{- $allObjects = merge $allObjects (dict "ServiceAccount" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "StorageClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "storage.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "CustomResource" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "PriorityClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "scheduling.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "Endpoints" (dict "HULL_TEMPLATE" $template)) }}

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
{{- $allObjects = merge $allObjects (dict "PodSecurityPolicy" (dict "HULL_TEMPLATE" $template "API_VERSION" "policy/v1beta1")) }}
{{- $allObjects = merge $allObjects (dict "ResourceQuota" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "NetworkPolicy" (dict "HULL_TEMPLATE" $template "API_VERSION" "networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "IngressClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "networking.k8s.io/v1")) }}

{{- /*
### Load rbac'ed objects
*/ -}}
{{- $template = "hull.object.base.rbac" }}
{{- $allObjects = merge $allObjects (dict "RoleBinding" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "ClusterRoleBinding" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1" "PARENT_TEMPLATE" "this.emptynamespace")) }}

{{- /*
### Load role objects
*/ -}}
{{- $template = "hull.object.base.role" }}
{{- $allObjects = merge $allObjects (dict "Role" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "ClusterRole" (dict "HULL_TEMPLATE" $template "API_VERSION" "rbac.authorization.k8s.io/v1" "PARENT_TEMPLATE" "this.emptynamespace")) }}
{{- /*

### Load webhook objects
*/ -}}
{{- $template = "hull.object.base.webhook" }}
{{- $allObjects = merge $allObjects (dict "MutatingWebhookConfiguration" (dict "HULL_TEMPLATE" $template "API_VERSION" "admissionregistration.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "ValidatingWebhookConfiguration" (dict "HULL_TEMPLATE" $template "API_VERSION" "admissionregistration.k8s.io/v1")) }}

{{- /*
### Load custom objects
*/ -}}
{{- $allObjects = merge $allObjects (dict "ConfigMap" (dict))  }}
{{- $allObjects = merge $allObjects (dict "Secret" (dict)) }}
{{- $allObjects = merge $allObjects (dict "Registry" (dict "API_KIND" "Secret")) }}
{{- $allObjects = merge $allObjects (dict "Service" (dict)) }}
{{- $allObjects = merge $allObjects (dict "Ingress" (dict "API_VERSION" "networking.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "CronJob" (dict "API_VERSION" "batch/v1")) }}
{{- $allObjects = merge $allObjects (dict "HorizontalPodAutoscaler" (dict "API_VERSION" "autoscaling/v2")) }}
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

{{- /*
### Get the default spec with key _HULL_OBJECT_TYPE_DEFAULT_ for the object to be merged with all instances
*/ -}}
{{- $defaultSpec := dict }}
{{- $defaultSpec = (index (index $rootContext.Values $hullRootKey).objects $lowerObjectType)._HULL_OBJECT_TYPE_DEFAULT_ }}

{{- range $objectKey, $spec := (index (index $rootContext.Values $hullRootKey).objects $lowerObjectType) }}
{{- if ne $objectKey "_HULL_OBJECT_TYPE_DEFAULT_" -}}
{{ if (gt (len (keys (default dict $spec))) 0) }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ $spec = merge $spec $defaultSpec }}

{{- /*
### Now render the result object instance
*/ -}}
{{- $objectSpec := dict }}
{{- $objectSpec = include "hull.util.merge" (merge (dict "PARENT_CONTEXT" $rootContext "PARENT_TEMPLATE" $parentTemplate "API_VERSION" (default $apiVersion $spec.apiVersion) "API_KIND" (default $apiKind $spec.apiKind) "COMPONENT" $objectKey "SPEC" $spec "DEFAULT_COMPONENT" $defaultSpec "HULL_ROOT_KEY" $hullRootKey "NO_SELECTOR" $noSelector "OBJECT_TYPE" $objectType) (dict "LOCAL_TEMPLATE" (printf "%s" $hullTemplate))) | fromYaml }}
{{- if (gt (len (keys (default dict $objectSpec))) 0) -}}
{{ toYaml $objectSpec }}

---
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}