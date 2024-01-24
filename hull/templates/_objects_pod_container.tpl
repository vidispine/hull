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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $containerType := (index . "CONTAINER_TYPE") -}}
{{- $keepHashsumAnnotations := (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.object.container.image" (dict "PARENT_CONTEXT" $parent "SPEC" $spec.image "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey "COMPONENT" $component "CONTAINER_TYPE" $containerType) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "env" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "env" "OBJECT_TEMPLATE" "hull.object.container.env" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "envFrom" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "envFrom" "OBJECT_TEMPLATE" "hull.object.container.envFrom" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "ports" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "ports" "OBJECT_TEMPLATE" "hull.object.container.ports" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType) | indent 2 }}
{{ include "hull.util.include.object" (dict "PARENT_CONTEXT" $parent "DEFAULT_SPEC" (dig "volumeMounts" dict (default dict $defaultSpec)) "SPEC" $spec "KEY" "volumeMounts" "OBJECT_TEMPLATE" "hull.object.container.volumeMounts" "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name" "image" "env" "envFrom" "ports" "volumeMounts")) | indent 2 }}
{{ end }}
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
{{- $component := default "" (index . "COMPONENT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $baseName := "" }}
{{- if (index $parent.Values $hullRootKey).config.general.errorChecks.containerImageValid -}}
{{- $details := printf "%s/%s/%s/%s" (index . "OBJECT_TYPE") (index . "OBJECT_INSTANCE_KEY") (index . "CONTAINER_TYPE") (index . "COMPONENT") }}
{{- if not $spec -}}
{{- $baseName = include "hull.util.error.message" (dict "ERROR_TYPE" "MISSING-IMAGE-SPEC" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- if (not (hasKey $spec "repository")) -}}
{{- $baseName = include "hull.util.error.message" (dict "ERROR_TYPE" "MISSING-IMAGE-REPOSITORY" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- $baseName = $spec.repository }}
{{- end -}}
{{- end -}}
{{- end -}}
{{ if (ne (default "" (index $parent.Values $hullRootKey).config.general.globalImageRegistryServer) "") }}
{{- $baseName = printf "%s/%s" (index $parent.Values $hullRootKey).config.general.globalImageRegistryServer $baseName }}
{{- else -}}
{{ if default false (index $parent.Values $hullRootKey).config.general.globalImageRegistryToFirstRegistrySecretServer }}
{{- $found := false }}
{{ if (gt (len (keys (default dict (index $parent.Values $hullRootKey).objects.registry))) 1) }}
{{- range $name, $specRegistry := (index $parent.Values $hullRootKey).objects.registry }}
{{- if (and (ne $name "_HULL_OBJECT_TYPE_DEFAULT_") (not $found)) }}
{{- $baseName = printf "%s/%s" (index (index $parent.Values $hullRootKey).objects.registry $name).server $baseName }}
{{- $found = true }}
{{- end }}
{{- end }}
{{- end }}
{{- else }}
{{ if (and (hasKey $spec "registry") (ne (printf "%s" $spec.registry) "")) }}
{{- $baseName = printf "%s/%s" $spec.registry $baseName }}{{- end }}
{{- end }}
{{- end }}
{{ if (and (hasKey $spec "tag") (ne (printf "%s" $spec.tag) "")) }}
{{- $baseName = printf "%s:%s" $baseName ($spec.tag | toString) }}
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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- $component := default nil (index . "COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
- {{ dict "name" $component | toYaml }}
{{ if hasKey $spec "valueFrom" }}
{{ include "hull.object.container.env.valueFrom" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec.valueFrom "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 2 }}
{{ end }}
{{ if hasKey $spec "value" }}
{{ printf "%s: %s" "value" ($spec.value | toString | quote) | indent 2 }}
{{ end }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name" "value" "valueFrom")) | indent 2 }}
{{- end -}}
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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
valueFrom:
{{ range $refKey, $refValue := $spec }}
  {{ $refKey }}:
{{ if $refValue.name }}
    name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $refValue.name "SPEC" $refValue "HULL_ROOT_KEY" $hullRootKey) }}    
{{ end }}
{{- $k8sOmit := list "name" -}}
{{- if (not $keepHashsumAnnotations) -}}
{{- $k8sOmit = append $k8sOmit "hashsumAnnotation" -}}
{{- end -}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $refValue "HULL_OBJECT_KEYS" $k8sOmit) | indent 4 }}
{{- end -}}
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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- $component := default nil (index . "COMPONENT") }}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
- {{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "configMapRef" "secretRef")) | indent 2 }}
{{ include "hull.object.container.envFrom.ref" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec "HULL_ROOT_KEY" $hullRootKey "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) |indent 2}}
{{ end }}
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
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{ range $refKey, $refValue := $spec }}
{{ if (or (eq $refKey "configMapRef") (eq $refKey "secretRef")) }}
{{ $refKey }}:
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $refValue.name "SPEC" $refValue "HULL_ROOT_KEY" $hullRootKey) }}   
{{- $k8sOmit := list "name" -}}
{{- if (not $keepHashsumAnnotations) -}}
{{- $k8sOmit = append $k8sOmit "hashsumAnnotation" -}}
{{- end -}} 
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $refValue "HULL_OBJECT_KEYS" $k8sOmit) | indent 2 }}
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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
{{- $k8sOmit := list -}}
{{- if (not $keepHashsumAnnotations) -}}
{{- $k8sOmit = append $k8sOmit "hashsumAnnotation" -}}
{{- end -}}
-{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" $k8sOmit) | indent 1 }}
{{ end }}
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
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $component := default nil (index . "COMPONENT") -}}
{{- if or (and (hasKey $spec "enabled") $spec.enabled) (and (not (hasKey $spec "enabled"))) -}}
- {{ dict "name" $component | toYaml }}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
{{ end }}
{{ end }}