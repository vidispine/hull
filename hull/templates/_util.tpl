{{- /*
| Purpose:  
|   
|   Merging function
|
*/ -}}
{{- define "hull.util.merge" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $apiVersion := (index . "API_VERSION") -}}
{{- $apiKind := (index . "API_KIND") -}}
{{- $component := (index . "COMPONENT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $localTemplate := (index . "LOCAL_TEMPLATE") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $overrides := fromYaml (include $template .) | default (dict ) -}}
{{- $tpl := fromYaml (include $localTemplate .) | default (dict ) -}}
{{- toYaml (merge $overrides $tpl) -}}
{{- end -}}

{{- define "hull.util.spec.merge.defaults" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{ $defaults := dict }}
{{ if and $objectType $spec }}
{{ if (and ((hasKey $parent.Values "hull") (hasKey (index $parent.Values $hullRootKey) "objects") (hasKey (index $parent.Values $hullRootKey).objects $objectType) (hasKey (index (index $parent.Values $hullRootKey).objects $objectType) "_HULL_OBJECT_TYPE_DEFAULT_"))) }}
{{ $defaults = index (index (index $parent.Values $hullRootKey).objects $objectType) "_HULL_OBJECT_TYPE_DEFAULT_" }}
{{ end }}
{{ end }}
{{ $merged := dict }}
{{ $merged := merge $merged $spec $defaults }}
{{ toYaml $merged }}
{{ end }}  

{{- define "hull.util.field" -}}
{{- $spec := (index . "SPEC") -}}
{{- $field := (index . "FIELD") -}}
{{- $indent := default 0 (index . "INDENT") -}}
{{- if hasKey $spec $field }}
{{ $field | indent $indent }}: {{ index $spec $field }}
{{- end }}
{{- end }}

{{- define "hull.util.field.oncondition" -}}
{{- $condition := (index . "CONDITION") -}}
{{- if $condition }}
{{ include "hull.util.field" . }}
{{- end }}
{{- end }}

{{- define "hull.util.yaml" -}}
{{- $spec := (index . "SPEC") -}}
{{- $field := (index . "FIELD") -}}
{{- $noKey := default false (index . "NO_KEY") -}}
{{- $indent := default 0 (index . "INDENT") -}}
{{- if hasKey $spec $field }}
{{ if not $noKey }}
{{ $field | indent $indent }}: 
{{ end }}
{{- if typeIs "[]interface {}" (index $spec $field) -}}
{{ toYaml (index $spec $field) | indent ($indent | int) }}
{{ else }}
{{ toYaml (index $spec $field) | indent ($indent | add1 | add1 | int) }}
{{- end }}
{{- end }}
{{- end }}

{{- define "hull.util.include.k8s" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullObjectBaseKeys := default (list "enabled" "labels" "annotations" "staticName") (index . "HULL_BASE_KEYS") }}
{{- $hullObjectKeys := default list (index . "HULL_OBJECT_KEYS") }}
{{- $spec := default nil (index . "SPEC") -}}
{{- $k8sSpec := dict }}
{{- $fields := concat $hullObjectBaseKeys $hullObjectKeys -}}
{{- range $key,$value := $spec -}}
{{- $t := dict -}}
{{- if has $key $fields -}}
{{- else }}
{{- $k8sSpec := set $k8sSpec $key $value -}}
{{- end -}}
{{- end -}}
{{ if (gt (len (keys $k8sSpec)) 0) }}
{{ toYaml $k8sSpec }}
{{- end -}}
{{- end -}}

{{- define "hull.util.include.object" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $defaultObjectSpec := default dict (index . "DEFAULT_SPEC") }}
{{- $objectTemplate := default dict (index . "OBJECT_TEMPLATE") }}
{{- $objectKey := (index . "KEY") }}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $isDefined := false }}
{{- range $key, $value := (index $spec (printf "%s" $objectKey)) }}
{{ if ne $key "_HULL_OBJECT_TYPE_DEFAULT_" }}
{{- $isDefined = true }}
{{ end }}
{{ end }}
{{- if $isDefined -}}
{{ $objectKey }}:
{{- range $key, $value := (index $spec (printf "%s" $objectKey)) }}
{{ if ne $key "_HULL_OBJECT_TYPE_DEFAULT_" }}
{{ if (gt (len (keys (default dict $value))) 0) }}
{{ $merged := dict }}
{{ $merged = merge $value $defaultObjectSpec }}  
{{ include (printf "%s" $objectTemplate) (dict "PARENT_CONTEXT" $parent "SPEC" $merged "ORIGIN_SPEC" $spec "COMPONENT" $key "HULL_ROOT_KEY" $hullRootKey) | indent 0 }}
{{ end }}
{{ end }}
{{ end }}
{{ else }}
{{ $objectKey }}: []
{{ end }}
{{ end }}

{{- define "hull.util.selector" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{ if hasKey $spec "selector" }}
selector: {{ $spec.selector }}
{{ else }}
{{ if not (default false (index . "NO_SELECTOR")) }}
selector:
  matchLabels:
{{ include "hull.metadata.labels.selector" . | indent 4 }}
{{ end }}
{{ end }}
{{ end }}