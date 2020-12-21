{{- /*
| Purpose:  
|   
|   Create a CronJob
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.cronjob" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $apiVersion := default "" (index . "API_VERSION") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.object.job.template" (merge (dict "SPEC" $spec.job "NO_HEADER" true "NO_TRANSFORMATIONS" true "NO_INCLUDE_K8S" true "DEFAULT_POD_BASE_PATH" $parent.Values.hull.objects.cronjob._HULL_OBJECT_TYPE_DEFAULT_.job.pod ) . ) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "job" "templateLabels" "templateAnnotations")) | indent 2 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Definition of a Job template
|
| Interface:
|
*/ -}}
{{- define "hull.object.job.template" -}}
jobTemplate:
{{ include "hull.object.base.pod" . | indent 2 }}
{{ end }}