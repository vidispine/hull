{{- /*
| Purpose:  
|   
|   Create a name.
|   <CHART> part can be overriden by hull.config.general.nameOverride
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.metadata.name"}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $base := default $parent.Chart.Name $parent.Values.hull.config.general.nameOverride -}}
{{- (printf "%s-%s" $base $component) | lower | trunc 54 | trimAll "-" -}}
{{- end -}}
