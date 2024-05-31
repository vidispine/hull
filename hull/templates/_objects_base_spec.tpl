{{- /*
| Purpose:  
|   
|   Create a object with a spec field
|   Contains a header and a spec with K8S schema validated properties
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.base.spec" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $forceEnabled := default false (index . "FORCE_ENABLED") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) $forceEnabled -}}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list)) | indent 2 }}
{{- end -}}
{{- end -}}