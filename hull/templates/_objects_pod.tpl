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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- $defaultPodBasePath := (index . "DEFAULT_COMPONENT") }}
{{- if hasKey . "DEFAULT_POD_BASE_PATH" }}
{{- $defaultPodBasePath = index . "DEFAULT_POD_BASE_PATH" }}
{{- end }}
{{- if (not (default false (eq $spec.pod nil))) }}
spec:
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "containers" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "containers" "OBJECT_TEMPLATE" "hull.object.container" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 -}}
{{- include "hull.object.pod.imagePullSecrets" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "initContainers" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "initContainers" "OBJECT_TEMPLATE" "hull.object.container" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 -}}
{{- include "hull.object.pod.serviceAccountName" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "pod" "volumes" "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultPodBasePath) "SPEC" $spec.pod "KEY" "volumes" "OBJECT_TEMPLATE" "hull.object.volume" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType) | indent 2 -}}
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
imagePullSecrets: 
{{ $spec.pod.imagePullSecrets | toYaml }}
{{- else -}}
{{ if (index $parent.Values $hullRootKey).config.general.createImagePullSecretsFromRegistries }}
{{ if (gt (len (keys (default dict (index $parent.Values $hullRootKey).objects.registry))) 1) }}
imagePullSecrets: 
{{- range $name, $specRegistry := (index $parent.Values $hullRootKey).objects.registry }}
{{- if (ne $name "_HULL_OBJECT_TYPE_DEFAULT_") }}
- name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" (index (index $parent.Values $hullRootKey).objects.registry $name) "COMPONENT" $name "HULL_ROOT_KEY" $hullRootKey) }}
{{- end }}
{{- end }}
{{- else }}
imagePullSecrets: []
{{- end }}
{{- end }}
{{- end }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Creates serviceAccountName for the pod.
|   If not explicitly specified, the default serviceaccount is used
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   DEFAULT_POD_BASE_PATH: Path to the pods default specification.
|
*/ -}}
{{- define "hull.object.pod.serviceAccountName" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ if hasKey $spec.pod "serviceAccountName" }}
serviceAccountName: {{ $spec.pod.serviceAccountName }}
{{ else }}
{{ if (index $parent.Values $hullRootKey).objects.serviceaccount.default.enabled }}
serviceAccountName: {{ include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "COMPONENT" "default" "HULL_ROOT_KEY" $hullRootKey) }}
{{ end }}
{{ end }}
{{ end }}
