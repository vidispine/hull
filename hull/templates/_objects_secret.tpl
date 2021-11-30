{{- /*
| Purpose:  
|   
|   Create a Secret.
|   Can include values from inlines: inline specification or from an external file in files:
|   External files can be incuded as is (no templating applied) or with templating expressions resolved.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.secret" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := (index (index $parent.Values $hullRootKey).objects ($objectType | lower))._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{- $hullValues := (index $parent.Values $hullRootKey) -}}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{ $renderedHullValues := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $hullValues "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{ $temp := dict "hull" $hullValues }}
{{ $parentClone := deepCopy $parent }}
{{ $parentClone = set $parentClone "Values" $temp }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.secret.data" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
{{- end -}}
{{- else }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.secret.data" . }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "data")) }}
{{- end }}
type: Opaque
{{- end -}}
{{ end }}


{{- /*
| Purpose:  
|   
|   Renders the K8S conform data section from the HULL input defined.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.secret.data" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
data:
{{ range $innerKey, $innerValue := $spec.data }}
{{- if or (and (hasKey $innerValue "enabled") $innerValue.enabled) (not (hasKey $innerValue "enabled")) -}}
{{ if hasKey $innerValue "inline" }}
{{ $innerKey | indent 2 }}: |-
{{ if $innerValue.noTemplating -}}
{{ default "" (toString $innerValue.inline) | b64enc | indent 4 }}
{{ else -}}
{{ default "" (tpl (printf "%s" (toString $innerValue.inline)) $parent) | b64enc | indent 4 }}
{{ end }}
{{ end }}
{{ if hasKey $innerValue "path" }}
{{ base $innerKey | indent 2 }}: |-
{{ if $innerValue.noTemplating }}
{{- toString ($parent.Files.Get (printf "%s" $innerValue.path) ) | b64enc | indent 4 -}}
{{- else -}}
{{- print (tpl (toString ($parent.Files.Get (printf "%s" $innerValue.path) ) ) $parent) | b64enc | indent 4 }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}