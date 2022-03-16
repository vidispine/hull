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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if (index $parent.Values $hullRootKey).config.general.rbac }}
{{ include "hull.object.base.plain" . }}
{{ end }}
{{ end }}