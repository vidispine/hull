{{- /*
| Purpose:  
|   
|   Create a Service.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.service" -}}
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
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (index $parent.Values $hullRootKey).objects.service._HULL_OBJECT_TYPE_DEFAULT_.ports._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "ports" "OBJECT_TEMPLATE" "hull.object.service.port") | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "ports")) | indent 2 }}
  selector: 
{{ include "hull.metadata.labels.selector" .  | indent 4 }}   
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create a port for Service ports:.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.service.port" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $component := default nil (index . "COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
{{ end }}
{{ end }}