{{- /*
| Purpose:  
|   
|   Write combined annotations: block from custom and default annotations
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|
*/ -}}
{{- define "hull.metadata.annotations" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $apiVersion := (index . "API_VERSION") -}}
{{- $apiKind := (index . "API_KIND") -}}
{{- $spec := (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ $annotations := dict }}
{{ $annotations = merge $annotations (include "hull.metadata.annotations.custom" . | fromYaml) }}
{{ if (gt (len (keys (index (index $parent.Values $hullRootKey).config.general.metadata.annotations "custom"))) 0) }}
{{ $annotations = merge $annotations (index $parent.Values $hullRootKey).config.general.metadata.annotations.custom }}
{{- end -}}
{{ if default false (index . "MERGE_TEMPLATE_METADATA") }}
{{ $annotations = merge $annotations ((include "hull.metadata.annotations.custom" (merge (dict "ANNOTATIONS_METADATA" "templateAnnotations") . ) | fromYaml)) }}
{{- end -}}
annotations:
{{ toYaml $annotations | indent 2 }}
{{- end -}}

{{- /*
{{ include "hull.metadata.annotations.hashes" . | indent 2 }}
*/ -}}


{{- /*
| Purpose:  
|   
|   Write out custom annotations
|
| Interface:
|
|   SPEC: The dictionary to work with
|   ANNOTATIONS_METADATA: The key in the SPEC holding the annotations
|
*/ -}}
{{- define "hull.metadata.annotations.custom" -}}
{{- $spec := (index . "SPEC") -}}
{{- $annotationsMetadata := default "annotations" (index . "ANNOTATIONS_METADATA") }}
{{ if (hasKey $spec $annotationsMetadata) }}
{{ if (gt (len (keys (index $spec $annotationsMetadata))) 0) }}
{{ toYaml (default dict (index $spec $annotationsMetadata)) }}
{{- end -}}
{{- end -}}
{{- end -}}


{{- /*
| Interface:
|   SPEC: The <hullObjectSpec>
| Purpose:  
|   Print the charts name and version for use in a label
*/ -}}
{{- define "hull.metadata.annotations.hashes" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $apiVersion := (index . "API_VERSION") -}}
{{- $apiKind := (index . "API_KIND") -}}
{{- $spec := (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- if eq $apiKind "Deployment" -}}
{{- $podSpec := include "hull.object.pod" . | fromYaml -}}
{{- $hashAnnotations := include "hull.metadata.annotations.hash"  (dict "PARENT_CONTEXT" $parent "SPEC" $podSpec.spec) -}}
{{- if (not (eq $hashAnnotations "")) -}}
{{- $hashAnnotations -}}
{{- end -}}
{{- /*
*/ -}}
{{- end -}}
{{- end -}}

{{- define "hull.metadata.annotations.hash" -}}
{{- $debug := false -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := (index . "SPEC") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{- $allFiles := dict -}}
{{- $volumeMount := (index . "VOLUME_MOUNT") -}}
{{- $volume := (index . "VOLUME") -}}  
{{- range $volume := $spec.volumes -}}
{{- if $debug -}}{{- $allFiles = set $allFiles "volumeName" $volume.name -}}{{- end -}}
  {{- range $container := concat (default list $spec.containers) (default list $spec.initContainers) -}}
{{- if $debug -}}{{- $allFiles = set $allFiles "containerName" $container.name -}}{{- end -}}
    {{- range $volumeMount := $container.volumeMounts -}}
      {{- if (eq $volumeMount.name $volume.name) -}} 
{{- if $debug -}}{{- $allFiles = set $allFiles "volumeMountName" $volumeMount.name -}}{{- end -}}
        {{- if (or $volume.configMap $volume.secret) -}}
          {{- $sources := dict -}}
          {{- if $volume.configMap -}}
            {{- $sources = dict "configMap" "name" -}}          
          {{- end -}}
          {{- if $volume.secret -}}
            {{- $sources = dict "secret" "secretName" -}}          
          {{- end -}}          
          {{- range $sourceKey, $sourceValue := $sources -}}   
{{- if $debug -}}{{- $allFiles = set $allFiles "source" $sourceKey -}}{{- end -}}
            {{- range $originKey, $originValue := (index (index $parent.Values $hullRootKey).objects ($sourceKey | lower)) -}}  
{{- if $debug -}}{{- $allFiles = set $allFiles "originKey" $originKey -}}{{- end -}} 
{{- if $debug -}}{{- $allFiles = set $allFiles "originValue" $originValue -}}{{- end -}} 
              {{- $fullName := include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $originKey "HULL_ROOT_KEY" $hullRootKey) -}}
              {{- $sourceSpecName := (index (index $volume $sourceKey) $sourceValue) -}}
{{- if $debug -}}{{- $allFiles = set $allFiles "sourceSpecName" $sourceSpecName -}}{{- end -}}
              {{- $sourceFields := dict "data" dict "files" dict -}}
              {{- $sourceFields := set $sourceFields "data" (default dict (index (index (index $parent.Values $hullRootKey).objects ($sourceKey | lower)) $originKey).data ) -}}
              {{- range $hullDataKey, $hullDataValue := (default dict (index (index (index $parent.Values $hullRootKey).objects ($sourceKey | lower)) $originKey).data) -}}
              {{- if hasKey $hullDataValue "inlines" -}}
              {{- $s := merge $sourceFields (dict "data" $hullDataValue.inlines) -}}
              {{- end -}}
              {{- if hasKey $hullDataValue "files" -}}
              {{- $s := set $sourceFields "files" $hullDataValue.files -}}
              {{- end -}}
              {{- end -}}
              {{- if eq (default "" $sourceSpecName) $fullName -}}
                {{- range $sourceTypeKey, $sourceTypeValue := $sourceFields -}}
                  {{- range $entryKey, $entryValue := $sourceTypeValue -}}
                    {{- $key := printf "hull.checksum.kubernetes.io/%s" (replace "." "_" $entryKey) -}}
                    {{- if hasKey $allFiles $key -}}
                    {{- else -}}
                      {{- if or (not $volumeMount.subPath) (eq (default "" $volumeMount.subPath) $sourceTypeKey) -}}
                        {{- $hash := "" -}}
                        {{- if (eq $sourceTypeKey "files") -}}
                          {{- $hash = print (tpl ($parent.Files.Get (printf "%s" $entryValue) ) $parent) | sha256sum -}}
                        {{- else -}}
                          {{- $hash = print "%s" $entryValue | sha256sum -}}
                        {{- end -}}
                        {{- $allFiles = set $allFiles $key $hash -}}
                      {{- end -}}
                    {{- end -}}
                  {{- end -}}
                {{- end -}}                         
              {{- end -}}              
            {{- end -}}    
          {{- end -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if (gt (len (keys $allFiles)) 0) -}}
{{- toYaml $allFiles -}}
{{- end -}}
{{- end -}}

