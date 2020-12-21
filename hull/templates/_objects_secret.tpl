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
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.secret" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $parent.Values.hull.objects.secret._HULL_OBJECT_TYPE_DEFAULT_.data._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "data" "OBJECT_TEMPLATE" "hull.object.secret.data") | indent 0 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
type: Opaque
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
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{ $name := (index . "NAME") }}
{{ $value := (index . "VALUE") }}
{{- $spec := default nil (index . "SPEC") -}}
{{ range $inlineKey, $inlineValue := $spec.inlines }}
{{ $inlineKey | indent 2 }}: |-
{{ default "" $inlineValue.data | b64enc | indent 4 }}
{{ end }}
{{ range $fileKey, $fileValue := $spec.files }}
{{ base $fileKey | indent 2 }}: |-
{{ if $fileValue.noTemplating }}
{{- ($parent.Files.Get (printf "%s" $fileValue.path) ) | b64enc | indent 4 -}}
{{- else -}}
{{- print (tpl ($parent.Files.Get (printf "%s" $fileValue.path) ) $parent) | b64enc | indent 4 }}
{{ end }}
{{ end }}
{{ end }}