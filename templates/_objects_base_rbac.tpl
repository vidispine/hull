{{- /*
| Purpose:  
|   
|   Create a plain object consisting only of header and K8S schema validated properties.
|   Only create the object if RBAC is enabled.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|
*/ -}}
{{- define "hull.object.base.rbac" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- if $parent.Values.hull.config.general.rbac }}
{{ include "hull.object.base.plain" . }}
{{ end }}
{{ end }}