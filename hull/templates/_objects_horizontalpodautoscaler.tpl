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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := (index (index $parent.Values $hullRootKey).objects ($objectType | lower))._HULL_OBJECT_TYPE_DEFAULT_.enabled -}}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $parent.Values.hull "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.object.horizontalpodautoscaler.scaleTargetRef" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.scaleTargetRef "HULL_ROOT_KEY" $hullRootKey) | indent 2}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "scaleTargetRef")) | indent 2 }}
{{- end -}}
{{- end -}}



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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
scaleTargetRef:
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.name "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey) }}    
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2}}
{{ end }}