{{- /*
| Purpose:  
|   
|   Create a object with a pod at its core. 
|   Contains a header, spec, selector, pod template and K8S schema validated properties
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|   NO_INCLUDE_K8S: The additional K8S object properties are not rendered
|
*/ -}}
{{- define "hull.object.base.pod" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := (index (index $parent.Values $hullRootKey).objects ($objectType | lower))._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.util.selector" . | indent 2 }}
{{ include "hull.object.pod.template" . | indent 2 }}
{{ if not (default false (index . "NO_INCLUDE_K8S")) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "pod" "templateLabels" "templateAnnotations")) | indent 2 }}
{{ end }}
{{ end }}
{{ end -}}