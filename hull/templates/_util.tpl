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
{{- $overrides := (include $template .) | fromYaml | default (dict ) -}}
{{- $tpl := (include $localTemplate .) | fromYaml | default (dict ) -}}
{{- if gt ($tpl | keys | len) 0 }}
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
{{- if $field | hasKey $spec }}
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
{{- $result = index $result $field -}}
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
{{- $hullObjectBaseKeys := (index . "HULL_BASE_KEYS") | default (list "enabled" "labels" "annotations" "staticName" "metadataNameOverride" "namespaceOverride" "sources" "conditionals") -}}
{{- $hullObjectKeys := (index . "HULL_OBJECT_KEYS") | default (list) -}}
{{- $spec := (index . "SPEC") | default nil -}}
{{- $k8sSpec := (dict) -}}
{{- $fields := concat $hullObjectBaseKeys $hullObjectKeys -}}
{{- range $key, $value := $spec -}}
  {{- if $fields | has $key | not -}}
    {{- $k8sSpec = set $k8sSpec $key $value -}}
  {{- end -}}
{{- end -}}
{{ if gt ($k8sSpec | keys | len) 0 }}
{{ $k8sSpec | toYaml }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:
|
|   Helper for printing out an HULL based key value dictionary to an Kubernetes array
|   Handles defaulting before rendering.
|   Array elements are ordered as determined by "hull.util.include.object.keys".
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
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $containerType := default "" (index . "CONTAINER_TYPE") -}}
{{- $renderEmptyArray := default (index $parent.Values $hullRootKey).config.general.render.emptyHullObjects (index . "RENDER_EMPTY_ARRAY")}}
{{- $sortByDependencies := default false (index . "SORT_BY_DEPENDENCIES") -}}
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
{{- $objects := index $spec (printf "%s" $objectKey) }}
{{- range $key := include "hull.util.include.object.keys" (dict "SPEC" $objects "DEFAULT_SPEC" $defaultObjectSpec "SORT_BY_DEPENDENCIES" $sortByDependencies) | fromJsonArray }}
{{- $value := index $objects $key }}
{{ if (gt (len (keys (default dict $value))) 0) }}
{{ $merged := dict }}
{{ $merged = merge $value $defaultObjectSpec }}
{{ if hasKey $merged "order" }}
{{ $merged = omit $merged "order" }}
{{ end }}
{{ include (printf "%s" $objectTemplate) (dict "PARENT_CONTEXT" $parent "SPEC" $merged "ORIGIN_SPEC" $spec "COMPONENT" $key "HULL_ROOT_KEY" $hullRootKey "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey "CONTAINER_TYPE" $containerType "KEEP_HASHSUM_ANNOTATIONS" $keepHashsumAnnotations) | indent 0 }}
{{ end }}
{{ end }}
{{ else }}
{{ if $renderEmptyArray }}
{{ $objectKey }}: []
{{ end }}
{{ end }}
{{ end }}



{{- /*
| Purpose:
|
|   Returns the keys of a HULL key value dictionary as JSON array in the order in which
|   they are rendered as Kubernetes array elements. Elements are sorted ascending by their
|   'order' property (default 0) and alphanumerically by key for equal 'order' values.
|   With SORT_BY_DEPENDENCIES, an element is never sorted before the enabled elements it
|   references via $(KEY) in its 'value' property. Elements in reference cycles fall back
|   to the plain sort order.
|
| Interface:
|
|   SPEC: The key value dictionary
|   DEFAULT_SPEC: The default specification applied to each element
|   SORT_BY_DEPENDENCIES: Whether to take $(KEY) references in 'value' properties into account
|
*/ -}}
{{- define "hull.util.include.object.keys" -}}
{{- $spec := default dict (index . "SPEC") -}}
{{- $defaultSpec := default dict (index . "DEFAULT_SPEC") -}}
{{- $sortByDependencies := default false (index . "SORT_BY_DEPENDENCIES") -}}
{{- $keys := without (keys $spec | sortAlpha) "_HULL_OBJECT_TYPE_DEFAULT_" -}}
{{- $orders := dict -}}
{{- $dependencies := dict -}}
{{- $isReordered := false -}}
{{- $active := dict -}}
{{- range $key := $keys -}}
{{- $value := default dict (index $spec $key) -}}
{{- $order := 0.0 -}}
{{- if hasKey $value "order" -}}
{{- $order = float64 $value.order -}}
{{- else if hasKey $defaultSpec "order" -}}
{{- $order = float64 $defaultSpec.order -}}
{{- end -}}
{{- $_ := set $orders $key $order -}}
{{- if ne $order 0.0 -}}
{{- $isReordered = true -}}
{{- end -}}
{{- $enabled := true -}}
{{- if hasKey $value "enabled" -}}
{{- $enabled = $value.enabled -}}
{{- else if hasKey $defaultSpec "enabled" -}}
{{- $enabled = $defaultSpec.enabled -}}
{{- end -}}
{{- if and $value $enabled -}}
{{- $_ := set $active $key true -}}
{{- end -}}
{{- end -}}
{{- if $sortByDependencies -}}
{{- range $key := keys $active | sortAlpha -}}
{{- $value := index $spec $key -}}
{{- $reference := "" -}}
{{- if hasKey $value "value" -}}
{{- $reference = toString $value.value -}}
{{- else if hasKey $defaultSpec "value" -}}
{{- $reference = toString $defaultSpec.value -}}
{{- end -}}
{{- $refs := list -}}
{{- range $match := regexFindAll `\$\([^)]*\)` (replace "$$" "" $reference) -1 -}}
{{- $ref := trimSuffix ")" (trimPrefix "$(" $match) -}}
{{- if and (hasKey $active $ref) (ne $ref $key) (not (has $ref $refs)) -}}
{{- $refs = append $refs $ref -}}
{{- end -}}
{{- end -}}
{{- if gt (len $refs) 0 -}}
{{- $_ := set $dependencies $key $refs -}}
{{- $isReordered = true -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if not $isReordered -}}
{{- $keys | toJson -}}
{{- else -}}
{{- $remaining := $keys -}}
{{- $placed := dict -}}
{{- $sorted := list -}}
{{- range $keys -}}
{{- $next := "" -}}
{{- $nextReady := false -}}
{{- range $key := $remaining -}}
{{- $ready := true -}}
{{- range $ref := index $dependencies $key | default list -}}
{{- if not (hasKey $placed $ref) -}}
{{- $ready = false -}}
{{- end -}}
{{- end -}}
{{- if or (eq $next "") (and $ready (not $nextReady)) (and (eq $ready $nextReady) (lt (index $orders $key) (index $orders $next))) -}}
{{- $next = $key -}}
{{- $nextReady = $ready -}}
{{- end -}}
{{- end -}}
{{- $sorted = append $sorted $next -}}
{{- $_ := set $placed $next true -}}
{{- $remaining = without $remaining $next -}}
{{- end -}}
{{- $sorted | toJson -}}
{{- end -}}
{{- end -}}



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
|   Function to merge sources with specs
|
*/ -}}
{{- define "hull.config.sources" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $lowerObjectType := (index . "OBJECT_TYPE") | lower -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $sourceType := (index . "SOURCE_TYPE") -}}
{{- $specKey := default "" (index . "SPEC_KEY") -}}
{{- $spec := (index . "SPEC") -}}
{{- $entry := $spec -}}
{{- if (ne $specKey "") -}}
{{- $entry = index $spec $specKey -}}
{{- end -}}
{{- $defaultTemplates := dig "sources" list $entry }}
{{- $defaultSpec := dict }}
{{- if (hasKey $entry "sources") -}}
{{- $defaultSpec = dict -}}
{{- range $source := $entry.sources -}}
{{- if not (hasKey (index (index $parent.Values $hullRootKey).config.templates $sourceType) $source) -}}
{{- fail (printf "No source with key %s found in hull.config.templates.%s" $source $sourceType) }}
{{- end -}}
{{- $_ := (mergeOverwrite $defaultSpec (omit (deepCopy (index (index (index $parent.Values $hullRootKey).config.templates $sourceType) $source)) "enabled")) -}}
{{- end -}}
{{- else -}}
{{- $_ := (mergeOverwrite $defaultSpec (omit (deepCopy (index (index (index $parent.Values $hullRootKey).config.templates $sourceType) "global")) "enabled")) -}}
{{- end -}}
{{- $_ := unset $entry "sources" -}}
{{- if (ne $specKey "") -}}
{{- $_ = set $spec $specKey (mergeOverwrite $defaultSpec (index $spec $specKey)) -}}
{{- else -}}
{{- $_ = (mergeOverwrite $defaultSpec $entry) | deepCopy -}}
{{- end -}}
{{ toYaml $defaultSpec }}
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
{{- $_ := (mergeOverwrite $defaultSpec (omit (deepCopy (index (index (index $parent.Values $hullRootKey).objects $lowerObjectType) $defaultTemplate)) "enabled")) -}}
{{- end -}}
{{- else -}}
{{- $_ := (mergeOverwrite $defaultSpec (deepCopy (index (index (index $parent.Values $hullRootKey).objects $lowerObjectType) "_HULL_OBJECT_TYPE_DEFAULT_"))) -}}
{{- end -}}
{{- end -}}
{{ toYaml $defaultSpec }}
{{ end }}



{{- /*
| Purpose:  
|   
|   Add an error to error list
|
*/ -}}
{{- define "hull.util.add.error" -}}
{{- $errorType := default "" (index . "ERROR_TYPE") -}}
{{- $errorMessage := default "" (index . "ERROR_MESSAGE") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectType := index . "OBJECT_TYPE" -}}
{{- $objectInstanceKey := index . "OBJECT_INSTANCE_KEY" -}}
{{- $existingErrorString := default "" (index . "EXISTING_ERROR_STRING") -}}
{{- if (not (hasKey (index (index $parent.Values $hullRootKey)) "_HULL_ERROR_")) -}}
{{- $_ := set (index (index $parent.Values $hullRootKey)) "_HULL_ERROR_" list -}}
{{- end -}}
{{- $composedErrorMessage := "" -}}
{{- if (ne $existingErrorString "") -}}
{{- $composedErrorMessage = $existingErrorString -}}
{{- else -}}
{{- $composedErrorMessage = include "hull.util.error.message" . -}}
{{- end -}}
{{- $found := false -}}
{{- $target := $composedErrorMessage -}}
{{- range $item := (index (index $parent.Values $hullRootKey) "_HULL_ERROR_") -}}
  {{- if (and (eq (print $item.ERROR_MESSAGE) (print $target))
              (eq (print $item.OBJECT_TYPE) (print $objectType))
              (eq (print $item.OBJECT_INSTANCE_KEY) (print $objectInstanceKey))) -}}
    {{- $found = true -}}
  {{- end -}}
{{- end -}}
{{- if not $found -}}
{{- $addedError := append (index (index $parent.Values $hullRootKey))._HULL_ERROR_ 
      (dict "ERROR_MESSAGE" $composedErrorMessage "OBJECT_TYPE" $objectType "OBJECT_INSTANCE_KEY" $objectInstanceKey) -}}
{{- $_ := set (index (index $parent.Values $hullRootKey)) "_HULL_ERROR_" $addedError -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create an error with message
|
*/ -}}
{{- define "hull.util.error.message" -}}
{{- $errorType := default "" (index . "ERROR_TYPE") -}}
{{- $errorMessage := default "" (index . "ERROR_MESSAGE") -}}
{{- printf "~%s:%s:%s" "_HULL_ERROR_" $errorType $errorMessage -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Error checking
*/ -}}
{{- define "hull.util.error.check" -}}
{{- $object := default "" (index . "OBJECT") -}}
{{- $lowerObjectType := default "" (index . "OBJECT_TYPE") -}}
{{- $errorMessage := "" -}}
{{- if typeIs "map[string]interface {}" $object -}}
  {{- range $key,$value := $object -}}
    {{- if typeIs "map[string]interface {}" $value -}}
       {{- include "hull.util.error.check" (dict "OBJECT" $value "OBJECT_TYPE" $lowerObjectType) -}}
    {{- end -}}
    {{- if typeIs "[]interface {}" $value -}}
      {{- include "hull.util.error.check" (dict "OBJECT" $value "OBJECT_TYPE" $lowerObjectType) -}}
    {{- end -}}
    {{- if typeIs "string" $value -}}
      {{- if (and $value (eq $lowerObjectType "secret") (regexMatch "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$" $value)) -}}
        {{- $value = $value | b64dec -}}
      {{- end -}}
      {{- if hasPrefix "~_HULL_ERROR_" $value -}}
        {{- $errors := regexSplit "~_HULL_ERROR_" (trimPrefix "~_HULL_ERROR_" $value) -1 -}}
        {{- range $error := $errors -}}
          {{- $errorParts := regexSplit ":" (trimAll "~" $error) -1 -}}
          {{- $errorMessage = printf "%s\n%s %s" $errorMessage "HULL failed with error" (index $errorParts 2) -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if typeIs "[]interface {}" $object -}}
   {{- range $value := $object -}}
    {{- include "hull.util.error.check" (dict "OBJECT" $value "OBJECT_TYPE" $lowerObjectType) -}}
  {{- end -}}
{{- end -}}
{{- if typeIs "string" $object -}}
  {{- if hasPrefix "~_HULL_ERROR_" $object -}}
    {{- $errors := regexSplit "~_HULL_ERROR_" (trimPrefix "~_HULL_ERROR_" $object) -1 -}}
    {{- range $error := $errors -}}
      {{- $errorParts := regexSplit ":" (trimAll "~" $error) -1 -}}
      {{- $errorMessage = printf "%s\n%s %s" $errorMessage "HULL failed with error" (index $errorParts 2) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{ $errorMessage }}
{{- end -}}


{{- /*
| Purpose:
|
|   Captures, before any transformation is resolved, whether the 'enabled' property of the
|   'default' ServiceAccount, Role and RoleBinding is still the HULL default that couples
|   them to 'hull.config.general.createDefaultRbacTriplet', and whether the RoleBinding's
|   'roleRef' and 'subjects' are still the HULL defaults.
|   Consumed by "hull.util.check.default.rbac.triplet" after transformations are resolved.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   HULL_ROOT_KEY: The root key of the HULL configuration
|
*/ -}}
{{- define "hull.util.check.default.rbac.triplet.raw" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objects := dig "objects" dict (default dict (index $parent.Values $hullRootKey)) -}}
{{- $defaultEnabled := "_HT?_HT*hull.config.general.createDefaultRbacTriplet" -}}
{{- $defaultRoleRef := dict "apiGroup" "rbac.authorization.k8s.io" "kind" "Role" "name" "_HT^default" -}}
{{- $defaultSubjects := list (dict "kind" "ServiceAccount" "name" "_HT^default" "namespace" "_HT**Release.Namespace") -}}
{{- $result := dict -}}
{{- range $objectType := list "serviceaccount" "role" "rolebinding" -}}
{{- $spec := default dict (dig $objectType "default" dict $objects) -}}
{{- $_ := set $result $objectType (dict "COUPLED" (and (kindIs "map" $spec) (eq (toString (index $spec "enabled")) $defaultEnabled))) -}}
{{- end -}}
{{- $roleBinding := default dict (dig "rolebinding" "default" dict $objects) -}}
{{- if kindIs "map" $roleBinding -}}
{{- $_ := set $result.rolebinding "CUSTOMIZED" (or (ne (toJson (index $roleBinding "roleRef")) (toJson $defaultRoleRef)) (ne (toJson (index $roleBinding "subjects")) (toJson $defaultSubjects))) -}}
{{- end -}}
{{ $result | toYaml }}
{{- end -}}



{{- /*
| Purpose:
|
|   Fails loudly instead of silently dropping configuration: when the 'default' ServiceAccount,
|   Role or RoleBinding is not rendered only because 'hull.config.general.createDefaultRbacTriplet'
|   is false, but the chart customized it (ServiceAccount 'annotations', Role 'rules',
|   RoleBinding 'roleRef' or 'subjects'), an error message is returned for each such object.
|   Setting 'enabled' explicitly on the object (true or false) is treated as a deliberate
|   decision and suppresses the error.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   HULL_ROOT_KEY: The root key of the HULL configuration
|   RAW: The result of "hull.util.check.default.rbac.triplet.raw"
|
*/ -}}
{{- define "hull.util.check.default.rbac.triplet" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $raw := default dict (index . "RAW") -}}
{{- $hull := default dict (index $parent.Values $hullRootKey) -}}
{{- $general := dig "config" "general" dict $hull -}}
{{- $objects := dig "objects" dict $hull -}}
{{- $errorMessage := "" -}}
{{- if not (dig "createDefaultRbacTriplet" false $general) -}}
{{- $customized := dict -}}
{{- $serviceAccount := default dict (dig "serviceaccount" "default" dict $objects) -}}
{{- if and (kindIs "map" $serviceAccount) (gt (len (default dict (index $serviceAccount "annotations"))) 0) -}}
{{- $_ := set $customized "serviceaccount" (list "annotations" "ServiceAccount" "has annotations") -}}
{{- end -}}
{{- if (dig "rbac" true $general) -}}
{{- $role := default dict (dig "role" "default" dict $objects) -}}
{{- if kindIs "map" $role -}}
{{- range $ruleKey, $rule := default dict (index $role "rules") -}}
{{- if and (ne $ruleKey "_HULL_OBJECT_TYPE_DEFAULT_") $rule -}}
{{- $_ := set $customized "role" (list "rules" "Role" "has rules") -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if dig "rolebinding" "CUSTOMIZED" false $raw -}}
{{- $_ := set $customized "rolebinding" (list "subjects" "RoleBinding" "has a customized roleRef or subjects") -}}
{{- end -}}
{{- end -}}
{{- range $objectType := list "serviceaccount" "role" "rolebinding" -}}
{{- if and (hasKey $customized $objectType) (dig $objectType "COUPLED" false $raw) -}}
{{- $details := index $customized $objectType -}}
{{- $errorMessage = printf "%s\nHULL failed with error (@Values.%s.objects.%s.default.%s) The 'default' %s %s but is not rendered because '%s.config.general.createDefaultRbacTriplet' is false. Set 'createDefaultRbacTriplet: true' to render the default ServiceAccount, Role and RoleBinding, or set 'enabled' explicitly on '%s.objects.%s.default' to decide for this object alone." $errorMessage $hullRootKey $objectType (index $details 0) (index $details 1) (index $details 2) $hullRootKey $hullRootKey $objectType -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{ $errorMessage }}
{{- end -}}
