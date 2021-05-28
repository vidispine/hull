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
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.base.spec" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list)) | indent 2 }}
{{ end }}