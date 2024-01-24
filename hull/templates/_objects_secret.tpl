{{- /*
| Purpose:  
|   
|   Create a Secret.
|   Can include values from inlines: inline specification or from an external file in files:
|   External files can be incuded as is (no templating applied) or with templating expressions resolved.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with

*/ -}}
{{- define "hull.object.secret" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- $hullValues := (index $parent.Values $hullRootKey) -}}
{{ $renderedHullValues := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $hullValues "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{ $temp := dict "hull" $hullValues }}
{{ $parentClone := deepCopy $parent }}
{{ $parentClone = set $parentClone "Values" $temp }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.secret.data" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
{{- end }}
type: {{ default "Opaque" $spec.type }}
{{ end }}


{{- /*
| Purpose:  
|   
|   Renders the K8S conform data section from the HULL input defined.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.secret.data" -}}
{{- include "hull.object.virtualfolder.data" (merge (dict "VIRTUAL_FOLDER_TYPE" "secret") .) }}
{{- end -}}