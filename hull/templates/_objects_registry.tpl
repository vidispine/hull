{{- /*
| Purpose:  
|   
|   Create a Registry Secret.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.registry" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
type: kubernetes.io/dockerconfigjson
{{- with $spec }}
data:
  .dockerconfigjson: "{{- printf "{\"auths\": {\"%s\": {\"auth\": \"%s\"}}}" $spec.server (printf "%s:%s" $spec.username $spec.password | b64enc) | b64enc }}"
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "server" "username" "password")) }}
{{ end }}
{{- end -}}