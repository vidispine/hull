{{- /*
| Purpose:  
|   
|   Create a ConfigMap
|   Can include values from inlines: inline specification or from an external file in files:
|   External files can be incuded as is (no templating applied) or with templating expressions resolved.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.configmap" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- $hullValues := (index $parent.Values $hullRootKey) -}}
{{ $renderedHullValues := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $hullValues "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{ $temp := dict "hull" $hullValues }}
{{ $parentClone := deepCopy $parent }}
{{ $parentClone = set $parentClone "Values" $temp }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.configmap.data" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec) }}
{{ include "hull.object.configmap.binarydata" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parentClone "SPEC" $spec "HULL_OBJECT_KEYS" (list "data" "binaryData")) }}
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
{{- define "hull.object.configmap.data" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
data:
{{ range $innerKey, $innerValue := $spec.data }}
{{- if or (and (hasKey $innerValue "enabled") $innerValue.enabled) (not (hasKey $innerValue "enabled")) -}}
{{ if hasKey $innerValue "inline" }}
{{ $innerValueString := "" }}
{{ if (or (not (kindIs "invalid" $innerValue.inline)) $parent.Values.hull.config.general.debug.renderNilWhenInlineIsNil) }}
{{ $innerValueString = toString $innerValue.inline }}
{{ end }}
{{ $innerKey | indent 2 }}: |-
{{ if $innerValue.noTemplating -}}
{{ default "" $innerValueString | indent 4 }}
{{ else -}}
{{ default "" (tpl (printf "%s" $innerValueString) $parent) | indent 4 }}
{{ end }}
{{ else }}
{{ if hasKey $innerValue "path" }}
{{ $pathExists := false }}
{{ range $path, $_ := $parent.Files.Glob $innerValue.path }}
{{ $pathExists = true }}
{{ end }}
{{ base $innerKey | indent 2 }}: |-
{{ if (and (not $pathExists) ($parent.Values.hull.config.general.debug.renderPathMissingWhenPathIsNonExistent)) -}}
{{ printf "<path missing: %s>" $innerValue.path | indent 4 }}
{{- else -}}
{{- if $innerValue.noTemplating -}}
{{ toString ($parent.Files.Get (printf "%s" $innerValue.path) ) | indent 4 }}
{{- else -}}
{{ print (tpl (toString ($parent.Files.Get (printf "%s" $innerValue.path) ) ) $parent) | indent 4 }}
{{- end -}}
{{ end }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}
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
{{- define "hull.object.configmap.binarydata" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if (hasKey $spec "binaryData") -}}
binaryData:
{{ range $innerKey, $innerValue := $spec.binaryData }}
{{ if typeIs "map[string]interface {}" $innerValue }}
{{- if or (and (hasKey $innerValue "enabled") $innerValue.enabled) (not (hasKey $innerValue "enabled")) -}}
{{ if hasKey $innerValue "path" -}}
{{ base $innerKey | indent 2 }}: |-
{{ toString ($parent.Files.Get (printf "%s" $innerValue.path) ) | indent 4 }}
{{ end }}
{{ end }}
{{- else -}}
{{ base $innerKey | indent 2 }}: {{ $innerValue }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}