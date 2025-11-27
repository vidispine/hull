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
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- $hullValues := (index $parent.Values $hullRootKey) -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
{{ include "hull.object.configmap.data" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey) }}
{{ include "hull.object.configmap.binarydata" (dict "PARENT_CONTEXT" $parent "SPEC" $spec) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "data" "binaryData")) }}
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
{{- include "hull.object.virtualfolder.data" (merge (dict "VIRTUAL_FOLDER_TYPE" "configmap") .) }}
{{- end -}}



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
{{ if hasKey $innerValue "inline" -}}
{{ base $innerKey | indent 2 }}: {{ $innerValue.inline }}
{{ end }}
{{ end }}
{{- else -}}
{{ base $innerKey | indent 2 }}: {{ $innerValue }}
{{ end }}
{{ end }}
{{ end }}
{{ end }}