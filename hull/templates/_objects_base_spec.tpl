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
{{- $enabledDefault := (index (index $parent.Values $hullRootKey).objects ($objectType | lower))._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list)) | indent 2 }}
{{- end -}}
{{- end -}}