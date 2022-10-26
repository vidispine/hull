{{- /*
| Purpose:  
|   
|   Create a plain object consisting only of header and K8S schema validated properties
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.base.plain" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := (index (index $parent.Values $hullRootKey).objects ($objectType | lower))._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list)) }}
{{- end -}}
{{- end -}}