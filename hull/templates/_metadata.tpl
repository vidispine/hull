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
{{- $spec := default dict (index . "SPEC") -}}
metadata:
{{ if not $noName }}
  name: {{ template "hull.metadata.fullname" . }}
{{ end }}
{{ if (hasKey $spec "namespaceOverride") }}
{{ if (eq $spec.namespaceOverride "") }}
{{ $details := printf "namespaceOverride for %s %s cannot be empty" (index . "OBJECT_TYPE") (index . "OBJECT_INSTANCE_KEY") }}
  namespace: {{ include "hull.util.error.message" (dict "ERROR_TYPE" "MISSING-NAMESPACE-OVERRIDE" "ERROR_MESSAGE" $details) }}
{{ else }}
  namespace: {{ $spec.namespaceOverride }}
{{ end }}
{{ else }}
{{ if (index $parent.Values $hullRootKey).config.general.namespaceOverride }}
  namespace: {{ (index $parent.Values $hullRootKey).config.general.namespaceOverride }}
{{ else }}
  namespace: {{ $parent.Release.Namespace }}
{{ end }}
{{ end }}
{{ include "hull.metadata.labels" . | indent 2 }}
{{ include "hull.metadata.annotations" . | indent 2 }}
{{- end -}}