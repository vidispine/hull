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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ $labels := dict }}
{{ $labels = merge $labels (include "hull.metadata.labels.custom" . | fromYaml) }}
{{ $labels = merge $labels ((include "hull.metadata.general.labels.object" .) | fromYaml) }}
{{ if (gt (len (keys (index (index $parent.Values $hullRootKey).config.general.metadata.labels "custom"))) 0) }}
{{ $labels = merge $labels (index $parent.Values $hullRootKey).config.general.metadata.labels.custom }}
{{- end -}}
{{ $labels = merge $labels ((include "hull.metadata.labels.selector" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "HULL_ROOT_KEY" $hullRootKey)) | fromYaml) }}
{{ if default false (index . "MERGE_TEMPLATE_METADATA") }}
{{ $labels = merge $labels ((include "hull.metadata.labels.custom" (merge (dict "LABELS_METADATA" "templateLabels") . ) | fromYaml)) }}
{{- end -}}
{{- $labelsStringify := dict }}
{{- range $labelKey, $labelValue := $labels -}}
{{- $_ := set $labelsStringify $labelKey ($labelValue | toString) -}}
{{- end -}}
{{ if (gt (len (keys (default dict $labelsStringify))) 0) }}
labels:
{{ toYaml $labelsStringify | indent 2 }}
{{- else -}}
{{ if (and (default false (index . "MERGE_TEMPLATE_METADATA")) (index $parent.Values $hullRootKey).config.general.render.emptyTemplateLabels) }}
labels: {}
{{- else -}}
{{- if (index $parent.Values $hullRootKey).config.general.render.emptyLabels -}}
labels: {}
{{- end -}}
{{- end -}}
{{- end -}}
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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
vidispine.hull/version: {{ default "" (index $parent.Values $hullRootKey).version }}
helm.sh/chart: {{ template "hull.metadata.chartref" (dict "PARENT_CONTEXT" $parent) }}
app.kubernetes.io/managed-by: {{ $parent.Release.Service | quote}}
app.kubernetes.io/version: {{ default ($parent.Chart.AppVersion | quote) ((index (index $parent.Values $hullRootKey).config.general.metadata.labels.common "app.kubernetes.io/version") | quote ) }}
app.kubernetes.io/part-of: {{ default "undefined" (index (index $parent.Values $hullRootKey).config.general.metadata.labels.common "app.kubernetes.io/part-of") }}
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
{{- $spec := default dict (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if $spec.selector -}}
{{- toYaml $spec.selector -}}
{{- else -}}
app.kubernetes.io/name: {{ template "hull.metadata.name" (dict "PARENT_CONTEXT" $parent "NAMEPREFIX" "" "COMPONENT" "" "HULL_ROOT_KEY" $hullRootKey) }}
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