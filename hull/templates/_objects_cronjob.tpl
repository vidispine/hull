{{- /*
| Purpose:  
|   
|   Create a CronJob
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.cronjob" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $apiVersion := default "" (index . "API_VERSION") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
spec:
{{ $jobConfig := merge . (dict "NO_HEADER" true "NO_SELECTOR" true "DEFAULT_POD_BASE_PATH" (dig "job" dict (default dict (index . "DEFAULT_COMPONENT"))) )  }}
{{ include "hull.object.job.template" $jobConfig | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "job")) | indent 2 }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Definition of a Job template
|
| Interface:
|
*/ -}}
{{- define "hull.object.job.template" -}}
{{- $spec := default nil (index . "SPEC") -}}
{{ $t := set . "SPEC" $spec.job }}
jobTemplate:
{{ include "hull.object.base.pod" . | indent 2 }}
{{ end }}