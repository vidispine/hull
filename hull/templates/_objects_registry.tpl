{{- /*
| Purpose:  
|   
|   Create a Registry Secret.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.registry" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
type: kubernetes.io/dockerconfigjson
{{- with $spec }}
data:
  .dockerconfigjson: "{{- printf "{\"auths\": {\"%s\": {\"auth\": \"%s\"}}}" $spec.server (printf "%s:%s" $spec.username $spec.password | b64enc) | b64enc }}"
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "server" "username" "password")) }}
{{ end }}
{{- end -}}
{{- end -}}