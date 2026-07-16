{{- /*
| Purpose:  
|   
|   Creates template: section for pods
|
| Interface:
|
|
*/ -}}
{{- define "hull.object.pod.template" -}}
template:
{{ include "hull.metadata" (merge (dict "NO_NAME" true "MERGE_TEMPLATE_METADATA" true) . ) | indent 2 }}
{{ include "hull.object.pod" . | indent 2 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Creates a pod.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   DEFAULT_POD_BASE_PATH: Path to the pods default specification.
|   API_KIND: The apiKind 
|
*/ -}}
{{- define "hull.object.pod" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- $defaultPodBasePath := (index . "DEFAULT_COMPONENT") }}
{{- if hasKey . "DEFAULT_POD_BASE_PATH" }}
{{- $defaultPodBasePath = index . "DEFAULT_POD_BASE_PATH" }}
{{- end }}
{{- if $spec.pod -}}
{{- $_ := set $spec "pod" (include "hull.config.sources" (merge (dict "SOURCE_TYPE" "pod" "SPEC_KEY" "pod") .) | fromYaml) -}}
spec:
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "containers" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "containers" "OBJECT_TEMPLATE" "hull.object.container" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey "CONTAINER_TYPE" "containers" "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 -}}
{{- include "hull.object.pod.imagePullSecrets" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "initContainers" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "initContainers" "OBJECT_TEMPLATE" "hull.object.container" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey "CONTAINER_TYPE" "initContainers" "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 -}}
{{- include "hull.object.pod.serviceAccountName" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "volumes" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "volumes" "OBJECT_TEMPLATE" "hull.object.volume" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey) | indent 2 -}}
{{- include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.pod "HULL_OBJECT_KEYS" (list "imagePullSecrets" "serviceAccountName" "containers" "initContainers" "volumes")) | indent 2 -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Creates image pull secrets for the pod.
|   If 'imagePullSecrets' exists as a field in the pod spec the value is used as is.
|   If 'imagePullSecrets' does not exists as a field, depending on the global 
|   parameter 'config.general.createImagePullSecretsFromRegistries' the created registries
|   are automatically added to each pod.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   DEFAULT_POD_BASE_PATH: Path to the pods default specification.
|
*/ -}}
{{- define "hull.object.pod.imagePullSecrets" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ if hasKey $spec.pod "imagePullSecrets" }}
{{ if (gt (len (default list $spec.pod.imagePullSecrets)) 0) }}
imagePullSecrets: 
{{ $spec.pod.imagePullSecrets | toYaml | indent 2 }}
{{- else -}}
{{- if (index $parent.Values $hullRootKey).config.general.render.emptyHullObjects -}}
imagePullSecrets: []
{{- end }}
{{- end }}
{{- else -}}
{{ if (index $parent.Values $hullRootKey).config.general.createImagePullSecretsFromRegistries }}
{{- $hasEnabledRegistry := false -}}
{{- range $name, $specRegistry := (index $parent.Values $hullRootKey).objects.registry -}}
{{- if and (ne $name "_HULL_OBJECT_TYPE_DEFAULT_") (ne $specRegistry.enabled false) -}}
{{- $hasEnabledRegistry = true -}}
{{- end -}}
{{- end -}}
{{ if and (gt (len (keys (default dict (index $parent.Values $hullRootKey).objects.registry))) 1) $hasEnabledRegistry }}
imagePullSecrets:
{{- range $name, $specRegistry := (index $parent.Values $hullRootKey).objects.registry }}
{{- if and (ne $name "_HULL_OBJECT_TYPE_DEFAULT_") (ne $specRegistry.enabled false) }}
- name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" (index (index $parent.Values $hullRootKey).objects.registry $name) "COMPONENT" $name "HULL_ROOT_KEY" $hullRootKey) }}
{{- end }}
{{- end }}
{{- else }}
{{- if (index $parent.Values $hullRootKey).config.general.render.emptyHullObjects -}}
imagePullSecrets: []
{{- end }}
{{- end }}
{{- end }}
{{- end }}
{{ end }}



{{- /*
| Purpose:
|
|   Computes the ServiceAccount name for a pod-mode per-workload service account.
|   Uses the workload spec for staticName resolution, objectType and instanceKey for uniqueness.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The pod-owning object's spec (for staticName)
|   OBJECT_TYPE: The object type (e.g. Deployment)
|   OBJECT_INSTANCE_KEY: The object instance key
|   HULL_ROOT_KEY: The hull root key
|
*/ -}}
{{- define "hull.object.pod.serviceaccount.podmode.name" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $instanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- include "hull.metadata.fullname" (dict
    "PARENT_CONTEXT" $parent
    "SPEC" $spec
    "COMPONENT" (printf "%s-%s" ($objectType | lower) $instanceKey)
    "HULL_ROOT_KEY" $hullRootKey) -}}
{{- end -}}



{{- /*
| Purpose:
|
|   Creates serviceAccountName for the pod.
|   Behaviour depends on config.general.createServiceAccounts:
|   - default: uses the default serviceaccount if enabled
|   - none:    no serviceAccountName is set
|   - pod:     sets a per-workload serviceaccount name
|   An explicit pod.serviceAccountName always takes precedence.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   OBJECT_TYPE: The object type
|   OBJECT_INSTANCE_KEY: The object instance key
|
*/ -}}
{{- define "hull.object.pod.serviceAccountName" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $createServiceAccounts := default "default" (index $parent.Values $hullRootKey).config.general.createServiceAccounts -}}
{{ if hasKey $spec.pod "serviceAccountName" }}
serviceAccountName: {{ $spec.pod.serviceAccountName }}
{{ else if eq $createServiceAccounts "pod" }}
serviceAccountName: {{ include "hull.object.pod.serviceaccount.podmode.name" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey "HULL_ROOT_KEY" $hullRootKey) }}
{{ else if eq $createServiceAccounts "default" }}
{{ if (index $parent.Values $hullRootKey).objects.serviceaccount.default.enabled }}
serviceAccountName: {{ include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "COMPONENT" "default" "HULL_ROOT_KEY" $hullRootKey) }}
{{ end }}
{{ end }}
{{ end }}