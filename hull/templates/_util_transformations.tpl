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
{{- if typeIs "map[string]interface {}" $source -}}
    {{- range $key,$value := $source -}}
        {{- if typeIs "map[string]interface {}" $value -}}
            {{- if hasKey $value "_HULL_TRANSFORMATION_" -}}
                {{- $params := $value._HULL_TRANSFORMATION_ -}}
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key) $params -}}
                {{- $valDict := fromYaml (include $value._HULL_TRANSFORMATION_._NAME_ $pass) -}}
                {{- $source := unset $source $key -}}
                {{- $source := merge $source $valDict -}}  
            {{- else -}}
                {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "CALLER" $source "CALLER_KEY" $key) -}}
            {{- end -}}
        {{- end -}}
        {{- if typeIs "[]interface {}" $value -}}
            {{- include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $value "CALLER" $source "CALLER_KEY" $key) -}}
        {{- end -}}
        {{- if typeIs "string" $value -}}
            {{- if (hasPrefix "_HULL_TRANSFORMATION_" $value) -}}
                {{- $paramsString := trimPrefix "_HULL_TRANSFORMATION_" $value -}}
                {{- $paramsSplitted := regexFindAll "(<<<[A-Z]+=.+?>>>)" $paramsString -1 -}}
                {{- $params := dict -}}
                {{- range $p := $paramsSplitted -}}
                    {{- $params = set $params (trimPrefix "<<<" (first (regexSplit "=" $p -1))) (trimSuffix ">>>" (last (regexSplit "=" $p -1))) -}}                
                {{- end -}}
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" $key) $params -}}
                {{- /* 
                */ -}}
                {{- $valDict := fromYaml (include ($params.NAME) $pass) -}} 
                {{- $source := unset $source $key -}}
                {{- $source := set $source $key (index $valDict $key) -}}  
            {{- end -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- if typeIs "[]interface {}" $source -}}
    {{- if typeIs "string" (first $source) }}
        {{- $transformedSource := list }}
        {{- range $listentry := $source -}}
            {{- if (hasPrefix "_HULL_TRANSFORMATION_" $listentry) -}}
                {{- $paramsString := trimPrefix "_HULL_TRANSFORMATION_" $listentry -}}
                {{- $paramsSplitted := regexFindAll "(<<<[A-Z]+=.+?>>>)" $paramsString -1 -}}
                {{- $params := dict -}}
                {{- range $p := $paramsSplitted -}}
                    {{- $params = set $params (trimPrefix "<<<" (first (regexSplit "=" $p -1))) (trimSuffix ">>>" (last (regexSplit "=" $p -1))) -}}                
                {{- end -}}
                {{- $pass := merge (dict "PARENT_CONTEXT" $parent "KEY" "key") $params -}}
                {{- /* 
                */ -}}
                {{- $valDict := fromYaml (include ($params.NAME) $pass) -}} 
                {{- $transformedSource = append $transformedSource (index $valDict "key") -}}  
            {{- else -}}
                {{- $transformedSource = append $transformedSource $listentry -}} 
            {{- end -}}
        {{- end -}}
        {{- $t2 := set $caller $callerKey $transformedSource -}}
    {{- else -}}
        {{- range $listentry := $source -}}
            {{- $newlistentry := include "hull.util.transformation" (dict "PARENT_CONTEXT" $parent "SOURCE" $listentry "CALLER" nil "CALLER_KEY" nil) -}}
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

{{- define "hull.util.transformation.custom2" -}}
{{- $key := (index . "KEY") -}}
{{ $content := (index . "CONTENT") }}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{ $key }}: {{  $content }}
{{- end -}}

{{- define "hull.util.transformation.custom" -}}
{{- $key := (index . "KEY") -}}
{{ $content := (index . "CONTENT") }}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{ $key }}: {{ tpl  $content (merge (dict "Template" $parent.Template "PARENT" $parent) .) }}
{{- end -}}