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
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $forceEnabled := default false (index . "FORCE_ENABLED") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) $forceEnabled -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.base.dynamic" . | indent 0 }}
{{- end -}}
{{- end -}}