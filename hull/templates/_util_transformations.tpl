{{- /*
| Purpose:  
|   
|   Iterates over a dictionary and sub dictionaries to apply transformations.
|
*/ -}}
{{- define "hull.util.transformation" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $source := (index . "SOURCE") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $caller := default nil (index . "CALLER") -}}
{{- $callerKey := default nil (index . "CALLER_KEY") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $shortForms := dict -}}
{{- $shortForms = set $shortForms "_HT?" (list "hull.util.transformation.bool" "CONDITION") -}}
{{- $shortForms = set $shortForms "_HT*" (list "hull.util.transformation.get" "REFERENCE") -}}
{{- $shortForms = set $shortForms "_HT!" (list "hull.util.transformation.tpl" "CONTENT") -}}
{{- $shortForms = set $shortForms "_HT^" (list "hull.util.transformation.makefullname" "COMPONENT") -}}
{{- $shortForms = set $shortForms "_HT&" (list "hull.util.transformation.selector" "COMPONENT") -}}
{{- $shortForms = set $shortForms "_HT/" (list "hull.util.transformation.include" "CONTENT") -}}
{{- if typeIs "map[string]interface {}" $source -}}
    {{- range $key,$value := $source -}}
        {{- $sourcePathKey := append $sourcePath $key }}
        {{- if typeIs "map[string]interface {}" $value -}}
            {{- $params := default nil $value._HULL_TRANSFORMATION_ -}}
            {{- range $sfKey, $sfValue := $shortForms -}}
                {{- if (hasKey $value $sfKey) -}}
                    {{- $params = dict "NAME" (first $sfValue) (last $sfValue) (first (values (index $value $sfKey))) -}}
                {{- end -}} 
            {{- end -}} 
            {{- if $params -}} 
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key "SOURCE_PATH" $sourcePathKey "HULL_ROOT_KEY" $hullRootKey) $params -}}
                {{- $others := omit $value "_HULL_TRANSFORMATION_" "_HULL_OBJECT_TYPE_DEFAULT_" "_HT?" "_HT*" "_HT!" "_HT^" "_HT&" "_HT/" -}}
                {{- $valDict := fromYaml (include $params.NAME $pass) -}}
                {{- $combined := $valDict }}
                {{- if (and (typeIs "map[string]interface {}" (index $valDict $key)) (gt (len (keys $others)) 0)) -}}
                  {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $others "SOURCE_PATH" $sourcePathKey "CALLER" $source "CALLER_KEY" $key "HULL_ROOT_KEY" $hullRootKey) -}}
                  {{- $combined = dict $key (merge $others (index $valDict $key)) }}
                {{- end -}}
                {{- $source := unset $source $key -}}
                {{- $source := merge $source $combined -}}
            {{- else -}}
                {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "SOURCE_PATH" $sourcePathKey "CALLER" $source "CALLER_KEY" $key "HULL_ROOT_KEY" $hullRootKey) -}}
            {{- end -}}
        {{- end -}}
        {{- if typeIs "[]interface {}" $value -}}
            {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "SOURCE_PATH" $sourcePathKey "CALLER" $source "CALLER_KEY" $key "HULL_ROOT_KEY" $hullRootKey) -}}
        {{- end -}}
        {{- if typeIs "string" $value -}}
            {{- $params := default nil nil -}}
            {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $value) (hasPrefix "_HT?" $value) (hasPrefix "_HT*" $value) (hasPrefix "_HT!" $value) (hasPrefix "_HT^" $value) (hasPrefix "_HT&" $value) (hasPrefix "_HT/" $value)) -}}
                {{- range $sfKey, $sfValue := $shortForms -}}
                    {{- if (hasPrefix $sfKey $value) -}}
                        {{- $params = dict "NAME" (first $sfValue) (last $sfValue) (trimPrefix $sfKey $value) -}}
                    {{- end -}} 
                {{- end -}} 
                {{- if (hasPrefix "_HULL_TRANSFORMATION_" $value) -}}
                    {{- $paramsString := trimPrefix "_HULL_TRANSFORMATION_" $value -}}
                    {{- $paramsSplitted := regexFindAll "(<<<[A-Z]+=.+?>>>)" $paramsString -1 -}}
                    {{- $params = dict -}}
                    {{- range $p := $paramsSplitted -}}
                        {{- $params = set $params (trimPrefix "<<<" (first (regexSplit "=" $p -1))) (trimSuffix ">>>" (trimPrefix (printf "%s=" (first (regexSplit "=" $p -1))) $p)) -}}
                    {{- end -}}
                {{- end -}}
            {{- end -}}             
            {{- if $params }}
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key "SOURCE_PATH" $sourcePathKey "HULL_ROOT_KEY" $hullRootKey) $params -}}
                {{- $valDict := fromYaml (include ($params.NAME) $pass) -}} 
                {{- $source := unset $source $key -}}
                {{- $source := set $source $key (index $valDict $key) -}}  
            {{- end -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- if typeIs "[]interface {}" $source -}}
    {{- if (and (typeIs "string" (first $source)) ) -}}
        {{- $listentry := first $source -}}
        {{- $params := default nil nil -}}
        {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $listentry) (hasPrefix "_HT?" $listentry) (hasPrefix "_HT*" $listentry) (hasPrefix "_HT!" $listentry) (hasPrefix "_HT^" $listentry) (hasPrefix "_HT&" $listentry) (hasPrefix "_HT/" $listentry)) -}}
            {{- range $sfKey, $sfValue := $shortForms -}}
                {{- if (hasPrefix $sfKey $listentry) -}}
                    {{- $params = dict "NAME" (first $sfValue) (last $sfValue)  (trimPrefix $sfKey $listentry) -}}
                {{- end -}} 
            {{- end -}} 
            {{- if (hasPrefix "_HULL_TRANSFORMATION_" $listentry) -}}
                {{- $paramsString := trimPrefix "_HULL_TRANSFORMATION_" $listentry -}}
                {{- $paramsSplitted := regexFindAll "(<<<[A-Z]+=.+?>>>)" $paramsString -1 -}}
                {{- $params = dict -}}
                {{- range $p := $paramsSplitted -}}
                    {{- $params = set $params (trimPrefix "<<<" (first (regexSplit "=" $p -1))) (trimSuffix ">>>" (trimPrefix (printf "%s=" (first (regexSplit "=" $p -1))) $p)) -}}
                {{- end -}}
            {{- end -}}
        {{- end -}}
        {{- if $params }}
            {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" "key" "SOURCE_PATH" $sourcePath "HULL_ROOT_KEY" $hullRootKey) $params -}}
            {{- $valDict := fromYaml (include ($params.NAME) $pass) -}} 
            {{- $t2 := set $caller $callerKey (index $valDict "key") -}}
        {{- else -}}
            {{- range $listentry := $source -}}
                {{- $newlistentry := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $listentry "CALLER" nil "CALLER_KEY" nil "SOURCE_PATH" $sourcePath "HULL_ROOT_KEY" $hullRootKey) -}}
            {{- end -}}
            {{- $t2 := set $caller $callerKey $source -}}
        {{- end -}}
    {{- else -}}
        {{- range $listentry := $source -}}
            {{- $newlistentry := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $listentry "CALLER" nil "CALLER_KEY" nil "SOURCE_PATH" $sourcePath "HULL_ROOT_KEY" $hullRootKey) -}}
        {{- end -}}
        {{- $t2 := set $caller $callerKey $source -}}
    {{- end -}}
{{- end -}}
{{- end -}}



{{- define "hull.util.transformation.ingress_classname_default" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $key := (index . "KEY") -}}
{{ $key }}: {{ printf "nginx-%s" ($parent.Release.Name | quote) }}
{{- end -}}



{{- define "hull.util.transformation.makefullname" -}}
{{- $key := (index . "KEY") -}}
{{ $key }}: {{ template "hull.metadata.fullname" . }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Determine additional parameters
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   REFERENCE: The key in dot-notation for which the value should be retrieved
|
*/ -}}
{{- define "hull.util.transformation.serialize.get" -}}
{{- $value := (index . "VALUE") -}}
{{- $serialize := false -}}
{{- $result := dict -}}
{{- range $serializer := list "none" "toJson" "toPrettyJson" "toRawJson" "toYaml" "toString" -}}
{{- if (hasPrefix (printf "%s|" $serializer) $value ) -}}
{{- $serialize = true -}}
{{- $result = set $result "serializer" $serializer -}}
{{- $result = set $result "remainder" ($value | trimPrefix (printf "%s|" $serializer)) -}}
{{- end -}}
{{- end -}}
{{- $result = set $result "serialize" $serialize -}}
{{- $result | toYaml -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Determince Conversion Type if present
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   REFERENCE: The key in dot-notation for which the value should be retrieved
|
*/ -}}
{{- define "hull.util.transformation.serialize" -}}
{{- $value := (index . "VALUE") -}}
{{- $serializer := (index . "SERIALIZER") -}}
{{- if (eq $serializer "toJson") -}}
{{- $value | toJson -}}
{{- else -}}
{{- if (eq $serializer "toPrettyJson") -}}
{{- $value | toPrettyJson -}}
{{- else -}}
{{- if (eq $serializer "toRawJson") -}}
{{- $value | toRawJson -}}
{{- else -}}
{{- if (eq $serializer "toYaml") -}}
{{- $value | toYaml -}}
{{- else -}}
{{- if (eq $serializer "toString") -}}
{{- $value | toString -}}
{{- else -}}
{{- $value -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Gets the value from a key in values.yaml given dot-notation.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   REFERENCE: The key in dot-notation for which the value should be retrieved
|   SOURCE_PATH: The path elements leading up to this field
|   RETURN_TEMPLATE_STRING: If true, returns a templating expression which can be 
|                           used with tpl to resolve this fields value. If false, 
|                           the resolved value itself is returned.
|
*/ -}}
{{- define "hull.util.transformation.get" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $key := (index . "KEY") -}}
{{- $reference := (index . "REFERENCE") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $returnTemplateString := default false (index . "RETURN_TEMPLATE_STRING") -}}
{{- $objectType := "" -}}
{{- $objectInstanceKey := "" -}}
{{- if (gt (len $sourcePath) 3) -}}
{{  if (eq (index $sourcePath 1) "objects") -}}
{{- $objectType = index $sourcePath 2 -}}
{{- $objectInstanceKey = index $sourcePath 3 -}}
{{- end -}}
{{- end -}}
{{- $templateString := "(index . \"$\").Values"  }}
{{- $current := $parent.Values -}}
{{- if hasPrefix "*" $reference -}}
{{- $reference = $reference | trimPrefix "*" -}}
{{- $current = toYaml $parent | fromYaml -}}
{{- $templateString = "(index . \"$\")"  }}
{{- end -}}
{{- $serializer := "" }}
{{- $getValue := include "hull.util.transformation.serialize.get" (dict "VALUE" $reference) | fromYaml -}}
{{- if $getValue.serialize -}}
{{- $reference = $getValue.remainder -}}
{{- if hasPrefix "*" $reference -}}
{{- $reference = $reference | trimPrefix "*" -}}
{{- $current = toYaml $parent | fromYaml -}}
{{- $templateString = "(index . \"$\")" }}
{{- end -}}
{{- $serializer = $getValue.serializer -}}
{{- end -}}
{{- $path := splitList "." $reference -}}
{{- $skipBroken := false}}
{{- $brokenPart := "" }}
{{- $details := "" -}}
{{- $isChartSpecialCase := false -}}
{{- if (eq (first $path) "Chart")  -}}
{{- $isChartSpecialCase = true -}}
{{- end -}}
{{- range $pathIndex, $pathElement := $path -}}
{{- if (and ($isChartSpecialCase) (eq $pathIndex 1)) -}}
{{- $pathElement = $pathElement | untitle -}}
{{- end -}}
{{- if eq $pathElement "§OBJECT_TYPE§" -}}
  {{- if ne $objectType "" -}}
    {{- $pathElement = $objectType -}}
  {{- else -}}
    {{- $skipBroken = true -}}
    {{- $brokenPart = $pathElement -}}
    {{- $details = printf "OBJECT_TYPE not set in current calling context, cannot get path %s" $reference }}
  {{- end -}}
{{- else -}}
  {{- if eq $pathElement "§OBJECT_INSTANCE_KEY§" -}}
    {{- if ne $objectInstanceKey "" -}}
      {{- $pathElement = $objectInstanceKey -}}
    {{- else -}}
      {{- $skipBroken = true -}}
      {{- $brokenPart = $pathElement -}}
      {{- $details = printf "OBJECT_INSTANCE_KEY not set in current calling context, cannot get path %s" $reference }}
    {{- end -}}
  {{- else -}}
    {{- $pathElement = regexReplaceAll "§" $pathElement "." }}
  {{- end -}}
{{- end -}}
{{- if (not $skipBroken) -}}
{{- if (regexMatch "^\\d+$" $pathElement) -}}
{{- $current = (index $current (int $pathElement)) -}}
{{- $templateString = printf "(index %s %s)" $templateString $pathElement }}
{{- else -}}
{{- if (or (hasKey $current $pathElement)) -}}
{{- $current = (index $current $pathElement) }}
{{- $templateString = printf "(index %s \"%s\")" $templateString $pathElement }}
{{- else -}}
{{- $skipBroken = true -}}
{{- $brokenPart = $pathElement -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if $skipBroken -}}
{{- if eq $details "" -}}
{{- $details = printf "Element %s in path %s was not found" $brokenPart $reference -}}
{{- end -}}
{{- if $returnTemplateString -}}
{{- include "hull.util.error.message" (dict "ERROR_TYPE" "HULL-GET-TRANSFORMATION-REFERENCE-INVALID" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- if $parent.Values.hull.config.general.debug.renderBrokenHullGetTransformationReferences -}}
{{ $key }}: BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element {{ $brokenPart }} in path {{ $reference }} was not found
{{- else }}
{{- if $parent.Values.hull.config.general.errorChecks.hullGetTransformationReferenceValid -}}
{{- $key }}: {{ include "hull.util.error.message" (dict "ERROR_TYPE" "HULL-GET-TRANSFORMATION-REFERENCE-INVALID" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- $key }}: ""
{{- end -}}
{{- end -}}
{{- end -}}
{{- else -}}
{{- if and (typeIs "string" $current) (not $current) }}
{{ $key }}: ""
{{- else -}}
{{- $convert := (include "hull.util.transformation.convert" (dict "SOURCE" $current "SERIALIZER" $serializer)) }}
{{- if (ne $serializer "") -}}
{{- $templateString = printf "(include \"hull.util.transformation.convert\" (dict \"SOURCE\" %s \"SERIALIZER\" \"%s\"))" $templateString $serializer }}
{{- end -}}
{{- if $returnTemplateString -}}
{{- $templateString -}}
{{- else -}}
{{ $key }}: {{ $convert }}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Simple conversion
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SOURCE: The Source Object
|
*/ -}}
{{- define "hull.util.transformation.convert" -}}
{{- $source := (index . "SOURCE") -}}
{{- $serializer := default "" (index . "SERIALIZER") -}}
{{- if typeIs "map[string]interface {}" $source -}}
{{- if (and (ne $serializer "") (ne $serializer "none")) -}}
{{- include "hull.util.transformation.serialize" (dict "VALUE" ($source) "SERIALIZER" $serializer) | toYaml -}}
{{- else -}}
{ 
  {{- range $k,$value := $source -}}
  {{ $k }}: {{ include "hull.util.transformation.convert" (dict "SOURCE" $value) -}},
  {{- end -}}
}
{{- end -}}
{{- else -}}
{{- if typeIs "[]interface {}" $source -}}
{{- if (and (ne $serializer "") (ne $serializer "none")) -}}
{{- include "hull.util.transformation.serialize" (dict "VALUE" ($source) "SERIALIZER" $serializer) | toYaml -}}
{{- else -}}
[
  {{- range $value := $source -}}
  {{- include "hull.util.transformation.convert" (dict "SOURCE" $value) -}},
  {{- end -}}
]
{{- end -}}
{{- else -}}
{{ $source }}
{{- end -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Process _HT* expressions
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   CONTENT: The string that describes the code which is subject to tpl
|
*/ -}}
{{- define "hull.util.process.get.paths" -}}
{{- $content := (index . "CONTENT") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $hits := regexFindAll "_HT\\*([A-Za-z\\._\\-\\d\\|\\*§]+)" $content -1 -}}
{{- $error := "" -}}
{{- range $hit := $hits -}}
{{- $rep := $hit | toString | replace "_HT*" "" -}}
{{- $replacement := include "hull.util.transformation.get" (merge (dict "REFERENCE" $rep "SOURCE_PATH" $sourcePath "RETURN_TEMPLATE_STRING" true) $parent) }}
{{- $errorMessage := include "hull.util.error.check" (dict "OBJECT" $replacement) -}}
{{- if (ne $errorMessage "") -}}
{{- $error = printf "%s%s" $error $replacement -}}
{{- else -}}
{{- $content = $content | replace $hit $replacement -}}
{{- end -}}
{{- end -}}
{{- (dict "error" $error "content" $content) | toYaml -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Construct a tpl string to process content
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   CONTENT: The string that describes the code which is subject to tpl
|
*/ -}}
{{- define "hull.util.process.tpl" -}}
{{- $key := (index . "KEY") -}}
{{- $content := (index . "CONTENT") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $objectType := "" -}}
{{- $objectInstanceKey := "" -}}
{{- if (gt (len $sourcePath) 3) -}}
{{  if (eq (index $sourcePath 1) "objects") -}}
{{- $objectType = index $sourcePath 2 -}}
{{- $objectInstanceKey = index $sourcePath 3 -}}
{{- end -}}
{{- end -}}
{{- $getProcessing := (include "hull.util.process.get.paths" (dict "CONTENT" $content "PARENT_CONTEXT" . "SOURCE_PATH" $sourcePath)) | fromYaml -}}
{{- if (ne $getProcessing.error "") -}}
{{ $key }}: {{ $getProcessing.error }}
{{- else -}}
{{ $key }}: {{ tpl $getProcessing.content (merge (dict "Template" $parent.Template "PARENT" $parent "$" $parent "OBJECT_INSTANCE_KEY" $objectInstanceKey "OBJECT_TYPE" $objectType) .) }}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Gets the value from a tpl expression run against the CONTENT string.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   CONTENT: The string that describes the code which is subject to tpl
|
*/ -}}
{{- define "hull.util.transformation.tpl" -}}
{{- $key := (index . "KEY") -}}
{{- $content := (index . "CONTENT") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- if (hasPrefix "*" $content) -}}
{{- $content = printf "%s %s %s" "{{" ($content | trimPrefix "*") "}}" -}}
{{- end -}}
{{- include "hull.util.process.tpl" (merge (dict "CONTENT" $content "SOURCE_PATH" $sourcePath) .) -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Gets the boolean value from a CONDITION via tpl.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   CONDITION: The condition to be checked against
|
*/ -}}
{{- define "hull.util.transformation.bool" -}}
{{- $key := (index . "KEY") -}}
{{- $content := (index . "CONDITION") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- if ($content | hasPrefix "/") -}}
{{- $includeContext := merge (dict "CONTENT" ($content | trimPrefix "/") "SOURCE_PATH" $sourcePath) . -}}
{{- $content = index (include "hull.util.transformation.include" $includeContext | fromYaml) $key -}}
{{- end -}}
{{- include "hull.util.process.tpl" (merge (dict "CONTENT" (printf "{{ if (%s) }}true{{ else }}false{{ end }}" $content) "SOURCE_PATH" $sourcePath) .) -}}
{{- end -}}


{{- /*
| Purpose:  
|   
|   Gets the selector block for a component.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   COMPONENT: The component used in naming
|
*/ -}}
{{- define "hull.util.transformation.selector" -}}
{{- $key := (index . "KEY") -}}
{{ $component := (index . "COMPONENT") }}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $name := include "hull.metadata.name" (dict "PARENT_CONTEXT" $parent "NAMEPREFIX" "" "COMPONENT" "") }}
{{- $instance := $parent.Release.Name | quote }}
{{- $component := default "undefined" $component }}
{{ $key }}: { "app.kubernetes.io/name": {{ $name }}, "app.kubernetes.io/instance": {{ $instance }}, "app.kubernetes.io/component": {{ $component}} }
{{- end -}}



{{- /*
| Purpose:  
|   
|   Calls an include and returns result
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   CONTENT: The content for the include function
|
*/ -}}
{{- define "hull.util.transformation.include" -}}
{{- $key := (index . "KEY") -}}
{{- $content := (index . "CONTENT") -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $serializer := "" -}}
{{- $objectType := "" -}}
{{- $objectInstanceKey := "" -}}
{{- if (gt (len $sourcePath) 3) -}}
{{  if (eq (index $sourcePath 1) "objects") -}}
{{- $objectType = index $sourcePath 2 -}}
{{- $objectInstanceKey = index $sourcePath 3 -}}
{{- end -}}
{{- end -}}
{{- $parts := regexSplit ":" ($content | trim) -1 -}}
{{- $parentContextSubmitted := false -}}
{{- $resultKey := "" -}}
{{- $includeName := ($parts | first) -}}
{{- $includeNameParts := include "hull.util.transformation.serialize.get" (dict "VALUE" $includeName) | fromYaml -}}
{{- if $includeNameParts.serialize -}}
{{- $includeName = $includeNameParts.remainder -}}
{{- $serializer = $includeNameParts.serializer -}}
{{- end -}}
{{- if (gt (len (regexSplit "/" $includeName -1)) 1) -}}
{{- $resultKey = (regexSplit "/" $includeName -1) | first -}}
{{- $includeName = (regexSplit "/" $includeName -1) | last -}}
{{- end -}}
{{- $call := printf "{{ include %s (dict " ($includeName | quote) -}}
{{- $isKey := true -}}
{{- range $entry := ($parts | rest) }}
{{- if (eq $entry "PARENT_CONTEXT") -}}
{{- $parentContextSubmitted = true -}}
{{- end -}}
{{- $value := $entry | replace "§" ":" -}}
{{- if $isKey -}}
{{- $value = ($entry | trimAll "\"" | quote) -}}
{{- $isKey = false -}}
{{- else -}}
{{- $isKey = true -}}
{{- end -}}
{{- $call = printf "%s%s " $call $value -}}
{{- end -}}
{{- if (not $parentContextSubmitted) -}}
{{- $call = printf "%s %s (index . \"$\")" $call ("PARENT_CONTEXT" | quote) -}}
{{- end -}}
{{- $call = printf "%s) }}" ($call | trim) -}}
{{- $tpl := tpl $call (merge (dict "Template" $parent.Template "PARENT" $parent "$" $parent "OBJECT_INSTANCE_KEY" $objectInstanceKey "OBJECT_TYPE" $objectType) .) -}}
{{- $result := dict -}}
{{- if (or (eq $serializer "") (eq $serializer "none")) -}}
{{- $result = $tpl | fromYaml -}}
{{- if (hasKey $result "Error")  -}}
{{- $result = $tpl -}}
{{- else -}}
{{- if (ne $resultKey "") -}}
{{- $result = index $result $resultKey -}}
{{- end -}}
{{- end -}}
{{- else -}}
{{- if (ne $resultKey "") -}}
{{- $result = index ($tpl | fromYaml) $resultKey -}}
{{- else -}}
{{- $result = $tpl | fromYaml -}}
{{- end -}}
{{- $result = include "hull.util.transformation.serialize" (dict "VALUE" $result "SERIALIZER" $serializer) -}}
{{- end -}}
{{ (dict $key $result) | toYaml }}
{{- end -}}
