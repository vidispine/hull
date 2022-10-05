{{- /*
| Purpose:  
|   
|   Iterates over a dictionary and sub dictionaries to apply transformations.
|
*/ -}}
{{- define "hull.util.transformation" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $source := (index . "SOURCE") -}}
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
        {{- if typeIs "map[string]interface {}" $value -}}
            {{- $params := default nil $value._HULL_TRANSFORMATION_ -}}
            {{- range $sfKey, $sfValue := $shortForms -}}
                {{- if (hasKey $value $sfKey) -}}}}
                    {{- $params = dict "NAME" (first $sfValue) (last $sfValue) (first (values (index $value $sfKey))) -}}
                {{- end -}} 
            {{- end -}} 
            {{- if $params -}} 
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key "HULL_ROOT_KEY" $hullRootKey) $params -}}
                {{- $others := omit $value "_HULL_TRANSFORMATION_" "_HULL_OBJECT_TYPE_DEFAULT_" "_HT?" "_HT*" "_HT!" "_HT^" "_HT&" "_HT/" -}}
                {{- $valDict := fromYaml (include $params.NAME $pass) -}}
                {{- $combined := $valDict }}
                {{- if (and (typeIs "map[string]interface {}" (index $valDict $key)) (gt (len (keys $others)) 0)) -}}
                {{- $combined = dict $key (merge $others (index $valDict $key)) }}
                {{- end -}}
                {{- $source := unset $source $key -}}
                {{- $source := merge $source $combined -}}
            {{- else -}}
                {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "CALLER" $source "CALLER_KEY" $key "HULL_ROOT_KEY" $hullRootKey) -}}
            {{- end -}}
        {{- end -}}
        {{- if typeIs "[]interface {}" $value -}}
            {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "CALLER" $source "CALLER_KEY" $key "HULL_ROOT_KEY" $hullRootKey) -}}
        {{- end -}}
        {{- if typeIs "string" $value -}}
            {{- $params := default nil nil -}}
            {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $value) (hasPrefix "_HT?" $value) (hasPrefix "_HT*" $value) (hasPrefix "_HT!" $value) (hasPrefix "_HT^" $value) (hasPrefix "_HT&" $value) (hasPrefix "_HT/" $value)) -}}
                {{- range $sfKey, $sfValue := $shortForms -}}
                    {{- if (hasPrefix $sfKey $value) -}}}}
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
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key "HULL_ROOT_KEY" $hullRootKey) $params -}}
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
                {{- if (hasPrefix $sfKey $listentry) -}}}}
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
            {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" "key" "HULL_ROOT_KEY" $hullRootKey) $params -}}
            {{- $valDict := fromYaml (include ($params.NAME) $pass) -}} 
            {{- $t2 := set $caller $callerKey (index $valDict "key") -}}
        {{- else -}}
            {{- range $listentry := $source -}}
                {{- $newlistentry := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $listentry "CALLER" nil "CALLER_KEY" nil "HULL_ROOT_KEY" $hullRootKey) -}}
            {{- end -}}
            {{- $t2 := set $caller $callerKey $source -}}
        {{- end -}}
    {{- else -}}
        {{- range $listentry := $source -}}
            {{- $newlistentry := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $listentry "CALLER" nil "CALLER_KEY" nil "HULL_ROOT_KEY" $hullRootKey) -}}
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
|   Gets the value from a key in values.yaml given dot-notation.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   REFERENCE: The key in dot-notation for which the value should be retrieved
|
*/ -}}
{{- define "hull.util.transformation.get" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $key := (index . "KEY") -}}
{{- $reference := (index . "REFERENCE") -}}
{{- $path := splitList "." $reference -}}
{{- $current := $parent.Values }}
{{- $skipBroken := false}}
{{- $brokenPart := "" }}
{{- range $pathElement := $path -}}
{{- $pathElement = regexReplaceAll "§" $pathElement "." }}
{{- if (not $skipBroken) -}}
{{- if (or (not $parent.Values.hull.config.general.debug.renderBrokenHullGetTransformationReferences) (hasKey $current $pathElement)) -}}
{{- $current = (index $current $pathElement) }}
{{- else -}}
{{- if $parent.Values.hull.config.general.debug.renderBrokenHullGetTransformationReferences -}}
{{- $skipBroken = true -}}
{{- $brokenPart = $pathElement -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if $skipBroken }}
{{ $key }}: BROKEN-HULL-GET-TRANSFORMATION-REFERENCE --> INVALID_PATH_ELEMENT {{ $brokenPart }} IN {{ $reference }}
{{- else -}}
{{- if and (typeIs "string" $current) (not $current) }}
{{ $key }}: ""
{{- else -}}
{{ $key }}: {{ (include "hull.util.transformation.convert" (dict "SOURCE" $current "KEY" $key)) }}
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
{{- if typeIs "map[string]interface {}" $source -}}
{ 
  {{- range $k,$value := $source -}}
  {{ $k }}: {{ include "hull.util.transformation.convert" (dict "SOURCE" $value) -}},
  {{- end -}}
}
{{- else -}}
{{- if typeIs "[]interface {}" $source -}}
[
  {{- range $value := $source -}}
  {{- include "hull.util.transformation.convert" (dict "SOURCE" $value) -}},
  {{- end -}}
]
{{- else -}}
{{ $source }}
{{- end -}}
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
{{ $content := (index . "CONTENT") }}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{ $key }}: {{ tpl  $content (merge (dict "Template" $parent.Template "PARENT" $parent "$" $parent) .) }}
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
{{ $content := (index . "CONDITION") }}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{ $key }}: {{ tpl  (printf "{{ if %s }}true{{ else }}false{{ end }}" $content) (merge (dict "Template" $parent.Template "PARENT" $parent "$" $parent) .) }}
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
{{- $parts := regexSplit ":" ($content | trim) -1 -}}
{{- $parentContextSubmitted := false -}}
{{- $resultKey := "" -}}
{{- $includeName := ($parts | first) -}}
{{- if (gt (len (regexSplit "/" ($parts | first) -1)) 1) -}}
{{- $resultKey = (regexSplit "/" ($parts | first) -1) | first -}}
{{- $includeName = (regexSplit "/" ($parts | first) -1) | last -}}
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
{{- $tpl := tpl $call (merge (dict "Template" $parent.Template "PARENT" $parent "$" $parent) .) -}}
{{- $result := $tpl | fromYaml -}}
{{- if (hasKey $result "Error")  -}}
{{- $result = $tpl -}}
{{- else -}}
{{- if (ne $resultKey "") -}}
{{- $result = index $result $resultKey -}}
{{- end -}}
{{- end -}}
{{ (dict $key $result) | toYaml }}
{{- end -}}