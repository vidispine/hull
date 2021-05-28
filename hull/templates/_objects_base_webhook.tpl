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
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $defaultWebhookBasePath := (index (index $parent.Values $hullRootKey).objects ($apiKind | lower))._HULL_OBJECT_TYPE_DEFAULT_.webhooks._HULL_OBJECT_TYPE_DEFAULT_ }}
{{- if not (default false (index . "NO_TRANSFORMATIONS")) }}
{{ $rendered := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $spec "HULL_ROOT_KEY" $hullRootKey) | fromYaml }}
{{- end }}
{{ template "hull.metadata.header" . }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultWebhookBasePath "SPEC" $spec "KEY" "webhooks" "OBJECT_TEMPLATE" "hull.object.base.webhook.webhooks" "HULL_ROOT_KEY" $hullRootKey) | indent 0 }}
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

