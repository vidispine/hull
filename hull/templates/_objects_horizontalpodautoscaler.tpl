{{- /*
| Purpose:  
|   
|   Create a HorizontalPodAutoscaler.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.horizontalpodautoscaler" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.object.horizontalpodautoscaler.scaleTargetRef" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.scaleTargetRef "HULL_ROOT_KEY" $hullRootKey) | indent 2}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "scaleTargetRef")) | indent 2 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the scaleTargetRef
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.horizontalpodautoscaler.scaleTargetRef" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
scaleTargetRef:
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.name "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey) }}    
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2}}
{{ end }}