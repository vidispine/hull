{{- /*
| Purpose:  
|   
|   Create an Ingress.
|   Subfields rules: and tls: are key value based.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.ingress" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $enabledDefault := dig "enabled" true (index . "DEFAULT_COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled")) $enabledDefault) -}}
{{ template "hull.metadata.header" . }}
spec:
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "tls" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict (index . "DEFAULT_COMPONENT"))) "SPEC" $spec "KEY" "tls" "OBJECT_TEMPLATE" "hull.object.ingress.tls" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "rules" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict (index . "DEFAULT_COMPONENT"))) "SPEC" $spec "KEY" "rules" "OBJECT_TEMPLATE" "hull.object.ingress.rules" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "rules" "tls")) | indent 2 }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create the tls: section for an ingress
|   If staticName is true, the secret name refered to is considered to be static
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.ingress.tls" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- secretName: {{ include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.secretName "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "secretName")) | indent 2 }}
{{ end }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the rules: section for an ingress
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.ingress.rules" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- host: {{ $spec.host }}
  http:
    paths:
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "http" "paths" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict (index . "DEFAULT_SPEC"))) "SPEC" $spec.http "KEY" "paths" "OBJECT_TEMPLATE" "hull.object.ingress.paths" "HULL_ROOT_KEY" $hullRootKey) | indent 4 }}
{{ end }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the paths: section for an ingress
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.ingress.paths" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- backend:
{{ if hasKey $spec.backend "service" }}
    service:
      name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.backend.service.name "SPEC" $spec.backend.service "HULL_ROOT_KEY" $hullRootKey) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.backend.service "HULL_OBJECT_KEYS" (list "name")) | indent 6 }}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "backend")) | indent 2 }}
{{ end }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the backend: section for an ingress
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.ingress.backend" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if hasKey $spec "service" }}   
service: 
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.service.name "SPEC" $spec.service "HULL_ROOT_KEY" $hullRootKey) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.service "HULL_OBJECT_KEYS" (list "name")) | indent 2}}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "service")) }}
{{ end }}