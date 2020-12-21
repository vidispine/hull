{{- /*
| Purpose:  
|   
|   Create a metadata: section including name, annotations and labels
|
| Interface:
|
|   NO_NAME: Optionally leave out name field
|
*/ -}}
{{ define "hull.metadata" -}}
{{ $noName := default false (index . "NO_NAME") }}
metadata:
{{ if not $noName }}
  name: {{ template "hull.metadata.fullname" . }}
{{ end }}
{{ include "hull.metadata.labels" . | indent 2 }}
{{ include "hull.metadata.annotations" . | indent 2 }}
{{- end -}}
