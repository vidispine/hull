{{- /*
| Purpose:  
|   
|   Create a Webhook.
|   Subfield webhooks: is key value based.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   NO_TRANSFORMATIONS: Don't execute the function that executes transformations
|
*/ -}}
{{- define "hull.object.base.webhook" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $apiKind := default "" (index . "API_KIND") -}}
{{- $defaultWebhookBasePath := (index $parent.Values.hull.objects ($apiKind | lower))._HULL_OBJECT_TYPE_DEFAULT_.webhooks._HULL_OBJECT_TYPE_DEFAULT_ }}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultWebhookBasePath "SPEC" $spec "KEY" "webhooks" "OBJECT_TEMPLATE" "hull.object.base.webhook.webhooks") | indent 0 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "webhooks")) | indent 0 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the webhooks: section for a webhook
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.base.webhook.webhooks" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
- name: {{ $spec.name }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
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
- host: {{ $spec.host }}
  http:
    paths:
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $parent.Values.hull.objects.ingress._HULL_OBJECT_TYPE_DEFAULT_.rules._HULL_OBJECT_TYPE_DEFAULT_.http.paths._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec.http "KEY" "paths" "OBJECT_TEMPLATE" "hull.object.ingress.paths") | indent 4 }}
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
- backend:
{{ if hasKey $spec.backend "service" }}
    service:
      name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.backend.service.name "SPEC" $spec.backend.service) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.backend.service "HULL_OBJECT_KEYS" (list "name")) | indent 6 }}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "backend")) | indent 2 }}
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
{{- if hasKey $spec "service" }}   
service: 
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.service.name "SPEC" $spec.service) }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.service "HULL_OBJECT_KEYS" (list "name")) | indent 2}}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "service")) }}
{{ end }}