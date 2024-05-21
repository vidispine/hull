{{- /*
| Purpose:  
|   
|   Checks whether a path exists.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.virtualfolder.path.exists" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $path := default "" (index . "PATH") -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Renders the K8S conform data section from the HULL input defined.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.virtualfolder.data" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $objectType := (index . "OBJECT_TYPE") -}}
{{- $objectInstanceKey := (index . "OBJECT_INSTANCE_KEY") -}}
{{- $virtualfolderType := default "configmap" (index . "VIRTUAL_FOLDER_TYPE") -}}
{{ $data := dict }}
{{- range $innerKey, $innerValue := $spec.data -}}
  {{- if or (and (hasKey $innerValue "enabled") $innerValue.enabled) (not (hasKey $innerValue "enabled")) -}}
    {{- $value := "" -}}
    {{- $serializer := "" -}}
    {{- $serializerByExtension := false }}
    {{- if hasKey $innerValue "serialization" -}}
      {{- $serializer = $innerValue.serialization -}}
    {{- else -}}
      {{- if (index $parent.Values.hull.config.general.serialization $virtualfolderType).enabled -}}
        {{- range $extension, $defaultSerializer := (index $parent.Values.hull.config.general.serialization $virtualfolderType).fileExtensions -}}
          {{- if hasSuffix (printf ".%s" $extension) $innerKey -}}
            {{- $serializer = $defaultSerializer -}}
            {{- $serializerByExtension = true }}
          {{- end -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
    {{- if hasKey $innerValue "inline" -}}
      {{- if (and (not (kindIs "invalid" $innerValue.inline)) (not (eq nil $innerValue.inline))) -}}
        {{- if (or (typeIs "map[string]interface {}" $innerValue.inline) (typeIs "[]interface {}" $innerValue.inline)) -}}
          {{- $value = $innerValue.inline -}}
        {{- else -}}
          {{- if $innerValue.noTemplating -}}
            {{- $value = toString ($innerValue.inline) -}}
          {{- else -}}
            {{- $value = (tpl (toString $innerValue.inline) $parent) -}}
          {{- end -}}
        {{- end -}}
      {{- else -}}
        {{- if $parent.Values.hull.config.general.debug.renderNilWhenInlineIsNil -}}
          {{- $value = "<nil>" -}}
        {{- else -}}
          {{- if $parent.Values.hull.config.general.errorChecks.virtualFolderDataInlineValid -}}
            {{- $details := printf "%s/%s/inline/%s" $objectType $objectInstanceKey $innerKey }}
            {{- $value = include "hull.util.error.message" (dict "ERROR_TYPE" "VIRTUAL-FOLDER-DATA-INLINE-INVALID" "ERROR_MESSAGE" $details) -}}
          {{- else -}}
            {{- $value = "" -}}
          {{- end -}}
        {{- end -}}
      {{- end -}}
    {{- else -}}
      {{- $pathExists := false -}}
      {{- range $path, $_ := $parent.Files.Glob $innerValue.path -}}
        {{- $pathExists = true -}}
      {{- end -}}
      {{- if (not $pathExists) -}}
        {{- if $parent.Values.hull.config.general.debug.renderPathMissingWhenPathIsNonExistent -}}
          {{- $value = printf "<path missing: %s>" $innerValue.path -}}
        {{- else -}}
          {{- if $parent.Values.hull.config.general.errorChecks.virtualFolderDataPathExists -}}
            {{- $details := printf "%s/%s/path/%s(%s)" $objectType $objectInstanceKey $innerKey $innerValue.path }}
            {{- $value = include "hull.util.error.message" (dict "ERROR_TYPE" "VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING" "ERROR_MESSAGE" $details) -}}
          {{- else -}}
            {{- $value = "" -}}
          {{- end -}}
        {{- end -}}
      {{- else -}}
        {{- $value = $parent.Files.Get (printf "%s" $innerValue.path) -}}
        {{- if not $innerValue.noTemplating -}}
          {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $value) (hasPrefix "_HT?" $value) (hasPrefix "_HT*" $value) (hasPrefix "_HT!" $value) (hasPrefix "_HT^" $value) (hasPrefix "_HT&" $value) (hasPrefix "_HT/" $value)) -}}
            {{- $pathContentTransformation := dict "content" $value -}}
            {{- $renderedHullValues := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $pathContentTransformation "HULL_ROOT_KEY" $hullRootKey) | fromYaml -}}
            {{- $value = index $pathContentTransformation "content" -}}
          {{- else -}}
            {{- $value = (tpl $value $parent) -}}
          {{- end -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
    {{- if (and (ne $serializer "") (ne $serializer "none")) -}}
      {{- if not (and $serializerByExtension (typeIs "string" $value)) -}}
        {{- if not (or (typeIs "map[string]interface {}" $value) (typeIs "[]interface {}" $value) $serializerByExtension) -}}
          {{- $value = fromYaml $value -}}
        {{- end -}}
        {{- $value = (include "hull.util.transformation.serialize" (dict "VALUE" $value "SERIALIZER" $serializer)) | toString -}}
      {{- end -}}
    {{- else -}}
      {{- $value = $value | toString -}}
    {{- end -}}
    {{- if (eq $virtualfolderType "secret") -}}
      {{- $value = b64enc $value -}}
    {{- end -}}
    {{- $data = set $data (base $innerKey) $value -}}
  {{- end -}}
{{- end -}}
{{- (dict "data" $data | toYaml ) -}}
{{- end -}}