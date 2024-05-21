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
{{ $parent := (index . "PARENT_CONTEXT") }}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
metadata:
{{ if not $noName }}
  name: {{ template "hull.metadata.fullname" . }}
{{ end }}
{{ if (index $parent.Values $hullRootKey).config.general.namespaceOverride }}
  namespace: {{ (index $parent.Values $hullRootKey).config.general.namespaceOverride }}
{{ else }}
  namespace: {{ $parent.Release.Namespace }}
{{ end }}
{{ include "hull.metadata.labels" . | indent 2 }}
{{ include "hull.metadata.annotations" . | indent 2 }}
{{- end -}}