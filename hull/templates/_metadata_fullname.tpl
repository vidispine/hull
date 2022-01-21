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
{{- $truncate := default 63 (index . "MAX_LENGTH") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $fullname := "" -}}
{{- if and $spec $spec.staticName -}}
{{- $fullname = default "" $component -}}
{{- $truncate = 10000 -}}
{{- end -}}
{{ if or ($fullname) (ne $fullname "") }}
{{-  (print $fullname) | lower | trunc $truncate | trimSuffix "-" -}}
{{ else -}}
{{- $base := "" -}}
{{- if (ne (default "" (index $parent.Values $hullRootKey).config.general.fullnameOverride) "") -}}
{{- $base = (index $parent.Values $hullRootKey).config.general.fullnameOverride -}}
{{- else -}}
{{- $base = printf "%s-%s" $parent.Release.Name $parent.Chart.Name -}}
{{- end -}}
{{- (printf "%s-%s" $base $component) | lower | trunc $truncate | trimAll "-" | trimAll "." -}}
{{ end }}
{{- end -}}
