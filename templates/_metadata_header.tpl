{{- /*
| Purpose:  
|   
|   Create an object header including all metadata (apiVersion, kind, metadata)
|
| Interface:
|
|   API_VERSION: The apiVersion of the object
|   API_KIND: The kind of the object
|   NO_HEADER: Optionally leave out apiVersion and kind
|
*/ -}}
{{- define "hull.metadata.header" -}}
{{- $apiVersion := default "" (index . "API_VERSION") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $noHeader := default false (index . "NO_HEADER") -}}
{{ if not $noHeader }}
apiVersion: {{ index . "API_VERSION" }}
kind: {{ index . "API_KIND" }}
{{ end }}
{{ include "hull.metadata" . }}
{{- end -}}