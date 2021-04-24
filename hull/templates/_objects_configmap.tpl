{{- /*
| Purpose:  
|   
|   Create a ConfigMap
|   Can include values from inlines: inline specification or from an external file in files:
|   External files can be incuded as is (no templating applied) or with templating expressions resolved.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.configmap" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{- $hullValues := $parent.Values.hull -}}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec) | fromYaml }}
{{- end }}
{{ $renderedHullValues := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $hullValues) | fromYaml }}
{{ $temp := dict "hull" $hullValues }}
{{ $parentClone := deepCopy $parent }}
{{ $parentClone = set $parentClone "Values" $temp }}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.configmap.data" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
{{- else }}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.configmap.data" . }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
{{- end }}
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
{{- define "hull.object.configmap.data" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
data:
{{ range $innerKey, $innerValue := $spec.data }}
{{ if hasKey $innerValue "inline" }}
{{ $innerKey | indent 2 }}: |-
{{ default "" $innerValue.inline | indent 4 }}
{{ end }}
{{ if hasKey $innerValue "path" }}
{{ base $innerKey | indent 2 }}: |-
{{ if $innerValue.noTemplating }}
{{- ($parent.Files.Get (printf "%s" $innerValue.path) ) | indent 4 -}}
{{- else -}}
{{- print (tpl ($parent.Files.Get (printf "%s" $innerValue.path) ) $parent) | indent 4 }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}