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
{{- $defaultPodBasePath := (index $parent.Values.hull.objects ($apiKind | lower))._HULL_OBJECT_TYPE_DEFAULT_.pod }}
{{- if hasKey . "DEFAULT_POD_BASE_PATH" }}
{{- $defaultPodBasePath = index . "DEFAULT_POD_BASE_PATH" }}
{{- end }}
spec:
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultPodBasePath.containers._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec.pod "KEY" "containers" "OBJECT_TEMPLATE" "hull.object.container") | indent 2 -}}
{{- include "hull.object.pod.imagePullSecrets" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultPodBasePath.initContainers._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec.pod "KEY" "initContainers" "OBJECT_TEMPLATE" "hull.object.container" ) | indent 2 -}}
{{- include "hull.object.pod.serviceAccountName" . | indent 2 -}}
{{- include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultPodBasePath.volumes._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec.pod "KEY" "volumes" "OBJECT_TEMPLATE" "hull.object.volume" ) | indent 2 -}}
{{- include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.pod "HULL_OBJECT_KEYS" (list "imagePullSecrets" "serviceAccountName" "containers" "initContainers" "volumes")) | indent 2 -}}
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
{{ if hasKey $spec.pod "imagePullSecrets" }}
imagePullSecrets: 
{{ $spec.pod.imagePullSecrets | toYaml }}
{{- else -}}
{{ if $parent.Values.hull.config.general.createImagePullSecretsFromRegistries }}
{{ if (gt (len (keys (default dict $parent.Values.hull.objects.registry))) 1) }}
imagePullSecrets: 
{{- range $name, $specRegistry := $parent.Values.hull.objects.registry }}
{{- if (ne $name "_HULL_OBJECT_TYPE_DEFAULT_") }}
- name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" (index $parent.Values.hull.objects.registry $name) "COMPONENT" $name) }}
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
{{ if hasKey $spec.pod "serviceAccountName" }}
serviceAccountName: {{ $spec.pod.serviceAccountName }}
{{ else }}
{{ if $parent.Values.hull.objects.serviceaccount.default.enabled }}
serviceAccountName: {{ include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "COMPONENT" "default") }}
{{ end }}
{{ end }}
{{ end }}
