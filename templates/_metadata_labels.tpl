{{- /*
| Purpose:  
|   
|   Write combined labels: block from custom and default annotations
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   PARENT_TEMPLATE: Metadata for the template section
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.metadata.labels" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $component := (index . "COMPONENT") -}}
{{ $labels := dict }}
{{ $labels = merge $labels (include "hull.metadata.labels.custom" . | fromYaml) }}
{{ $labels = merge $labels ((include "hull.metadata.general.labels.object" .) | fromYaml) }}
{{ if (gt (len (keys (index $parent.Values.hull.config.general.metadata.labels "custom"))) 0) }}
{{ $labels = merge $labels $parent.Values.hull.config.general.metadata.labels.custom }}
{{- end -}}
{{ $labels = merge $labels ((include "hull.metadata.labels.selector" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component)) | fromYaml) }}
{{ if default false (index . "MERGE_TEMPLATE_METADATA") }}
{{ $labels = merge $labels ((include "hull.metadata.labels.custom" (merge (dict "LABELS_METADATA" "templateLabels") . ) | fromYaml)) }}
{{- end -}}
labels:
{{ toYaml $labels | indent 2 }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Write combined labels: block from custom and default annotations
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|
*/ -}}
{{- define "hull.metadata.general.labels.object" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
helm.sh/chart: {{ template "hull.metadata.chartref" (dict "PARENT_CONTEXT" $parent) }}
app.kubernetes.io/managed-by: {{ $parent.Release.Service | quote}}
app.kubernetes.io/version: {{ default ($parent.Chart.AppVersion | quote) ((index $parent.Values.hull.config.general.metadata.labels.common "app.kubernetes.io/version") | quote ) }}
app.kubernetes.io/part-of: {{ default "undefined" (index $parent.Values.hull.config.general.metadata.labels.common "app.kubernetes.io/part-of") }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Write selector labels.
|   If SPEC contains a selector field it overwrites the default behavior
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   COMPONENT: The instance name to be used in creating names
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.metadata.labels.selector" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := (index . "COMPONENT") -}}
{{- $spec := (index . "SPEC") -}}
{{- if $spec.selector -}}
{{- toYaml $spec.selector -}}
{{- else -}}
app.kubernetes.io/name: {{ template "hull.metadata.name" (dict "PARENT_CONTEXT" $parent "NAMEPREFIX" "" "COMPONENT" "") }}
app.kubernetes.io/instance:  {{ $parent.Release.Name | quote }}
app.kubernetes.io/component: {{ default "undefined" $component }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Write custom labels.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   LABELS_METADATA: The key in the SPEC holding the labels
|
*/ -}}
{{- define "hull.metadata.labels.custom" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $labelsMetadata := default "labels" (index . "LABELS_METADATA") }}
{{ if (hasKey $spec $labelsMetadata) }}
{{ if (gt (len (keys (index $spec $labelsMetadata))) 0) }}
{{ toYaml (default dict (index $spec $labelsMetadata)) }}
{{- end -}}
{{- end -}}
{{- end -}}