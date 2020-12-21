{{- /*
| Purpose:  
|   
|   Create a chart reference from parent charts name and version
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|
*/ -}}
{{- define "hull.metadata.chartref" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- replace "+" "_" $parent.Chart.Version | printf "%s-%s" $parent.Chart.Name -}}
{{- end -}}
