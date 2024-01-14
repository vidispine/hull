{{- /*
| Purpose:
|
|   Global Merging function
|
*/ -}}
{{- define "hull.util.merge" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $apiVersion := (index . "API_VERSION") -}}
{{- $apiKind := (index . "API_KIND") -}}
{{- $component := (index . "COMPONENT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $localTemplate := (index . "LOCAL_TEMPLATE") -}}
{{- $hullRootKey := (index . "HULL_ROOT_KEY") | default "hull" -}}
{{- $overrides := (include $template .) | fromYaml | default (dict) -}}
{{- $tpl := (include $localTemplate .) | fromYaml | default (dict) -}}
{{- if gt ($tpl | keys | len) 0 -}}
{{- (merge $overrides $tpl) | toYaml -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:
|
|   Helper for printing out a key value entry
|
*/ -}}
{{- define "hull.util.field" -}}
{{- $spec := (index . "SPEC") -}}
{{- $field := (index . "FIELD") -}}
{{- $indent := (index . "INDENT") | default 0 -}}
{{- if $field | hasKey $spec -}}
{{- (dict $field (index $spec $field)) | toYaml | indent $indent -}}
{{- end }}
{{- end }}



{{- /*
| Purpose:
|
|   Helper for printing out a key value entry on a given condition
|
*/ -}}
{{- define "hull.util.field.oncondition" -}}
{{- $condition := (index . "CONDITION") -}}
{{- if $condition }}
{{ include "hull.util.field" . }}
{{- end }}
{{- end }}



{{- /*
| Purpose:
|
|   Helper for printing out a dict to YAML
|
*/ -}}
{{- define "hull.util.yaml" -}}
{{- $spec := (index . "SPEC") -}}
{{- $field := (index . "FIELD") -}}
{{- $noKey := (index . "NO_KEY") | default false -}}
{{- $indent := (index . "INDENT") | default 0 -}}
{{- $result := (dict) -}}
{{- if $field | hasKey $spec -}}
{{- $result = index $result $field
{{- if eq $noKey true -}}
{{- $result = dict $field $result -}}
{{- end -}}
{{- $result | toYaml | indent $indent -}}
{{- end }}
{{- end }}



{{- /*
| Purpose:
|
|   Helper for printing out an object from the Kubernetes specification.
|   Fields not to be rendered (because handled by HULL) are provided in HULL_OBJECT_KEYS
|
*/ -}}
{{- define "hull.util.include.k8s" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullObjectBaseKeys := default (list "enabled" "labels" "annotations" "staticName" "metadataNameOverride" "sources") (index . "HULL_BASE_KEYS") }}
{{- $hullObjectKeys := default list (index . "HULL_OBJECT_KEYS") }}
{{- $spec := default nil (index . "SPEC") -}}
{{- $k8sSpec := dict }}
{{- $fields := concat $hullObjectBaseKeys $hullObjectKeys -}}
{{- range $key,$value := $spec -}}
{{- $t := dict -}}
{{- if has $key $fields -}}
{{- else }}
{{- $k8sSpec := set $k8sSpec $key $value -}}
{{- end -}}
{{- end -}}
{{ if (gt (len (keys $k8sSpec)) 0) }}
{{ toYaml $k8sSpec }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:
|
|   Helper for printing out an HULL based key value dictionary to an Kubernetes array
|   Handles defaulting before rendering.
|
*/ -}}
{{- define "hull.util.include.object" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $defaultObjectSpec := default dict (index . "DEFAULT_SPEC") }}
{{- $objectTemplate := default dict (index . "OBJECT_TEMPLATE") }}
{{- $objectKey := (index . "KEY") }}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $keepHashsumAnnotations := default false (index . "KEEP_HASHSUM_ANNOTATIONS") -}}
{{- $isDefined := false }}
{{- if hasKey $spec (printf "%s" $objectKey) }}
{{- range $key, $value := (index $spec (printf "%s" $objectKey)) }}
{{ if ne $key "_HULL_OBJECT_TYPE_DEFAULT_" }}
{{- $isDefined = true }}
{{ end }}
{{ end }}
{{ end }}
{{- if $isDefined -}}
{{ $objectKey }}:
{{- range $key, $value := (index $spec (printf "%s" $objectKey)) }}
{{ if ne $key "_HULL_OBJECT_TYPE_DEFAULT_" }}
{{ if (gt (len (keys (default dict $value))) 0) }}
{{ $merged := dict }}
{{ $merged = merge $value $defaultObjectSpec }}
{{ include (printf "%s" $objectTemplate) (dict "PARENT_CONTEXT" $parent "SPEC" $merged "ORIGIN_SPEC" $spec "COMPONENT" $key "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 0 }}
{{ end }}
{{ end }}
{{ end }}
{{ else }}
{{ $objectKey }}: []
{{ end }}
{{ end }}



{{- /*
| Purpose:
|
|   Create a selector dictionary
|
*/ -}}
{{- define "hull.util.selector" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{ if hasKey $spec "selector" }}
selector: {{ $spec.selector }}
{{ else }}
{{ if not (default false (index . "NO_SELECTOR")) }}
selector:
  matchLabels:
{{ include "hull.metadata.labels.selector" . | indent 4 }}
{{ end }}
{{ end }}
{{ end }}



{{- /*
| Purpose:
|
|   Central function to determine defaults for an object instance
|
*/ -}}
{{- define "hull.objects.defaults" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $lowerObjectType := (index . "OBJECT_TYPE") | lower -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $defaultSpec := dict }}
{{- $defaultSpec = (index (index $parent.Values $hullRootKey).objects $lowerObjectType)._HULL_OBJECT_TYPE_DEFAULT_ }}
{{- if (or (gt (len (keys (default dict $spec))) 0) (not (kindIs "invalid" $spec))) -}}
{{- $defaultTemplates := dig "sources" list $spec }}
{{- if (hasKey $spec "sources") -}}
{{- $defaultSpec = dict -}}
{{- range $defaultTemplate := $defaultTemplates -}}
{{- if (regexMatch "^.*\\[.*$" $defaultTemplate) -}}
{{- $lowerObjectType = (regexSplit "\\[" $defaultTemplate -1) | last | replace "]" "" | lower -}}
{{- $defaultTemplate = (regexSplit "\\[" $defaultTemplate -1) | first | lower -}}
{{- end -}}
{{- if not (hasKey (index $parent.Values $hullRootKey).objects $lowerObjectType) -}}
{{- fail (printf "No object type %s in hull.objects" $lowerObjectType) }}
{{- end -}}
{{- if not (hasKey (index (index $parent.Values $hullRootKey).objects $lowerObjectType) $defaultTemplate) -}}
{{- fail (printf "No object instance %s in hull.objects %s" $defaultTemplate $lowerObjectType) }}
{{- end -}}
{{- $defaultSpec = (merge (omit (index (index (index $parent.Values $hullRootKey).objects $lowerObjectType) $defaultTemplate) "enabled") $defaultSpec) -}}
{{- end -}}
{{- else -}}
{{- $defaultSpec = (merge (index (index (index $parent.Values $hullRootKey).objects $lowerObjectType) "_HULL_OBJECT_TYPE_DEFAULT_") $defaultSpec) -}}
{{- end -}}
{{- end -}}
{{ toYaml $defaultSpec }}
{{ end }}
