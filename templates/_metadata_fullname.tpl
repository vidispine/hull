{{- /*
| Purpose:  
|   
|   Create a full name.
|   Can be forced with 'staticName' to create a static name from COMPONENT only.
|   <RELEASE>-<CHART> part can be overriden by static hull.config.general.fullnameOverride
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   COMPONENT: The instance name to be used in creating names
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.metadata.fullname"}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $fullname := "" -}}
{{- if and $spec $spec.staticName -}}
{{- $fullname = default "" $component -}}
{{- end -}}
{{ if or ($fullname) (ne $fullname "") }}
{{-  (print $fullname) | lower | trunc 54 | trimSuffix "-" -}}
{{ else -}}
{{- $base := default (printf "%s-%s" $parent.Release.Name $parent.Chart.Name) $parent.Values.hull.config.general.fullnameOverride -}}  
{{- (printf "%s-%s" $base $component) | lower | trunc 54 | trimAll "-" -}}
{{ end }}  
{{- end -}}
