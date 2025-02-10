{{- /*
| Purpose:  
|   
|   Create the targetRefs: section for a BackendLBPolicy
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.base.gateway.api.gateway.listener" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ dict "name" $component | toYaml }}
{{ if hasKey $spec "tls" }}
{{ include "hull.object.base.gateway.api.gateway.listener.tls" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "tls" dict (default dict $defaultSpec)) "COMPONENT" $component "SPEC" $spec.tls "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ end }}
{{ if hasKey $spec "allowedRoutes" }}
{{ include "hull.object.base.gateway.api.gateway.listener.allowedroutes" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "allowedRoutes" dict (default dict $defaultSpec)) "COMPONENT" $component "SPEC" $spec.allowedRoutes "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "tls" "allowedRoutes")) | indent 2 }}
{{ end }}
{{ end }}



{{- define "hull.object.base.gateway.api.gateway.listener.allowedroutes" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
allowedRoutes:
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "kinds" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "kinds" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "kinds")) | indent 2 }}
{{ end }}



{{- define "hull.object.base.gateway.api.gateway.listener.tls" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
tls:
{{ if hasKey $spec "frontendValidation" }}
{{ include "hull.object.base.gateway.api.gateway.listener.frontendvalidation" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "frontendValidation" dict (default dict $defaultSpec)) "COMPONENT" $component "SPEC" $spec.frontendValidation "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ end }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "certificateRefs" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "certificateRefs" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "frontendValidation" "certificateRefs")) | indent 2 }}
{{ end }}



{{- define "hull.object.base.gateway.api.gateway.listener.frontendvalidation" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") }}
frontendValidation:
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "caCertificateRefs" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "caCertificateRefs" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "caCertificateRefs")) | indent 2 }}
{{ end }}



{{- define "hull.object.base.gateway.api.extended.backendrefs" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") }}
- {{ if hasKey $spec "filters" }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "filters" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "filters" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "filters")) | indent 2 }}
{{ end }}



{{- define "hull.object.base.gateway.api.extended.route.rules" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ if hasKey $spec "matches" }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "matches" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "matches" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ end }}
{{ if hasKey $spec "filters" }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "filters" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "filters" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ end }}
{{ if hasKey $spec "backendRefs" }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "backendRefs" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "backendRefs" "OBJECT_TEMPLATE" "hull.object.base.gateway.api.extended.backendrefs" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "matches" "filters" "backendRefs")) | indent 2 }}
{{ end }}
{{ end }}



{{- define "hull.object.base.gateway.api.simple.route.rules" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (not (hasKey $spec "enabled")) -}}
- {{ if hasKey $spec "backendRefs" }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "backendRefs" "_HULL_OBJECT_TYPE_DEFAULT_" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "backendRefs" "OBJECT_TEMPLATE" "hull.object.base.dynamic.simple.array" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2}}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "backendRefs")) | indent 2 }}
{{ end }}
{{ end }}