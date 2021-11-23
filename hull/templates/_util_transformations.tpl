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
{{- $hullRootKey := (index . "HULL_ROOT_KEY") -}}
{{- $shortForms := dict -}}
{{- $shortForms = set $shortForms "_HT?" (list "hull.util.transformation.bool" "CONDITION") -}}
{{- $shortForms = set $shortForms "_HT*" (list "hull.util.transformation.get" "REFERENCE") -}}
{{- $shortForms = set $shortForms "_HT!" (list "hull.util.transformation.tpl" "CONTENT") -}}
{{- $shortForms = set $shortForms "_HT^" (list "hull.util.transformation.makefullname" "COMPONENT") -}}
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
                {{- $others := omit $value "_HULL_TRANSFORMATION_" "_HULL_OBJECT_TYPE_DEFAULT_" "_HT?" "_HT*" "_HT!" "_HT^"}}
                {{- $valDict := fromYaml (include $params.NAME $pass) -}}
                {{- $combined := dict $key (merge $others (index $valDict $key)) }}
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
            {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $value) (hasPrefix "_HT?" $value) (hasPrefix "_HT*" $value) (hasPrefix "_HT!" $value) (hasPrefix "_HT^" $value)) -}}
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
        {{- if (or (hasPrefix "_HULL_TRANSFORMATION_" $listentry) (hasPrefix "_HT?" $listentry) (hasPrefix "_HT*" $listentry) (hasPrefix "_HT!" $listentry) (hasPrefix "_HT^" $listentry)) -}}
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
{{- range $pathElement := $path -}}
{{- $current = (index $current $pathElement) }}
{{- end -}}
{{ $key }}: {{ $current }}
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