{{- /*
| Purpose:  
|   
|   Create an object with list or dict fields.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- /*
| Purpose:  
|   
|   Create a Role.
|   Subfield rules: is key value based.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.base.dynamic" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $dynamicFields := default dict (index . "DYNAMIC_FIELDS") -}}
{{- $defaultComponent := index . "DEFAULT_COMPONENT" -}} 
{{- $skipDictFields := list }}
{{- range $field, $objectTemplate := $dynamicFields }}
{{- $defaultFieldBasePath := dig $field "_HULL_OBJECT_TYPE_DEFAULT_" dict $defaultComponent }}
{{- $fieldExists := hasKey $spec $field -}}
{{- if $fieldExists -}}
{{- if typeIs "map[string]interface {}" (index $spec $field) -}}
{{ $skipDictFields = append $skipDictFields $field }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultFieldBasePath "SPEC" $spec "KEY" $field "OBJECT_TEMPLATE" $objectTemplate "HULL_ROOT_KEY" $hullRootKey) | indent 0 }}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if (eq (len $skipDictFields) 0) -}}
{{- $skipDictFields = append $skipDictFields "" -}}
{{- end -}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" $skipDictFields) | indent 0 }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create a simple array from a Dictionary
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.base.dynamic.simple.array" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "")) | indent 2 }}
{{ end }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create a simple array from a Dictionary and set name to component
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.base.dynamic.simple.array.name.from.component" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
{{ end }}
{{ end }}