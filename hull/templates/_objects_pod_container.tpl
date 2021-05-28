{{- /*
| Purpose:  
|   
|   Create a container specification.
|   Applies to containers: and initContainers: alike.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|   DEFAULT_SPEC: The specification with the defaults for the container. Either the containers or initContainers defaults.
|
*/ -}}
{{- define "hull.object.container" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := (index . "DEFAULT_SPEC") -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.object.container.image" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.image) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultSpec.env._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "env" "OBJECT_TEMPLATE" "hull.object.container.env" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultSpec.envFrom._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "envFrom" "OBJECT_TEMPLATE" "hull.object.container.envFrom" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultSpec.ports._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "ports" "OBJECT_TEMPLATE" "hull.object.container.ports" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" $defaultSpec.volumeMounts._HULL_OBJECT_TYPE_DEFAULT_ "SPEC" $spec "KEY" "volumeMounts" "OBJECT_TEMPLATE" "hull.object.container.volumeMounts" "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name" "image" "env" "envFrom" "ports" "volumeMounts")) | indent 2 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create the image: of the container.
|   Applies to containers: and initContainers: alike.
|   Three components are: registry, repository and tag.
|
| Interface:
|
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.container.image" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $baseName := $spec.repository }}
{{ if (and (hasKey $spec "registry") (ne (printf "%s" $spec.registry) "")) }}
{{- $baseName = printf "%s/%s" $spec.registry $baseName }}
{{ end }}
{{ if (and (hasKey $spec "tag") (ne (printf "%s" $spec.tag) "")) }}
{{- $baseName = printf "%s:%s" $baseName $spec.tag }}
{{ end }}
image: {{ $baseName }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create env: section items
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.container.env" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $component := default nil (index . "COMPONENT") -}}
- {{ dict "name" $component | toYaml }}
{{ if hasKey $spec "valueFrom" }}
{{ include "hull.object.container.env.valueFrom" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec.valueFrom "HULL_ROOT_KEY" $hullRootKey) | indent 2 }}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name" "valueFrom")) | indent 2 }}
{{- end -}}




{{- /*
| Purpose:  
|   
|   Create env: section item from a valueFrom: specification
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.container.env.valueFrom" -}}
{{ $parent := (index . "PARENT_CONTEXT") }}
{{ $spec := (index . "SPEC") }}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
valueFrom:
{{ range $refKey, $refValue := $spec }}
  {{ $refKey }}:
{{ if $refValue.name }}
    name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $refValue.name "SPEC" $refValue "HULL_ROOT_KEY" $hullRootKey) }}    
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $refValue "HULL_OBJECT_KEYS" (list "name")) | indent 4 }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create an envFrom: item
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.container.envFrom" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $component := default nil (index . "COMPONENT") }}
- {{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "configMapRef" "secretRef")) | indent 2 }}
{{ include "hull.object.container.envFrom.ref" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey) |indent 2}}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create an envFrom: reference
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.container.envFrom.ref" -}}
{{ $name := (index . "NAME") }}
{{ $value := (index . "VALUE") }}
{{ $parent := (index . "PARENT_CONTEXT") }}
{{ $spec := (index . "SPEC") }}
{{ $component :=  (index . "COMPONENT") }}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{ range $refKey, $refValue := $spec }}
{{ if (or (eq $refKey "configMapRef") (eq $refKey "secretRef")) }}
{{ $refKey }}:
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $refValue.name "SPEC" $refValue "HULL_ROOT_KEY" $hullRootKey) }}    
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $refValue "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
{{ end }}
{{ end }}
{{ end }}

{{- /*
| Purpose:  
|   
|   Create an volumeMount: item
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.container.volumeMounts" -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
-{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list)) | indent 1 }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Create a ports: item
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.container.ports" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $component := default nil (index . "COMPONENT") -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
{{ end }}