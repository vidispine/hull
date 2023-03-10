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
{{ end }}
{{ if default false (index . "MERGE_TEMPLATE_METADATA") }}
  {{ $annotations = merge $annotations ((include "hull.metadata.annotations.custom" (merge (dict "ANNOTATIONS_METADATA" "templateAnnotations") . ) | fromYaml)) }}
  {{ $annotations = merge $annotations (include "hull.metadata.annotations.hash" . | fromYaml) }}
{{ end }}
annotations:
{{ toYaml $annotations | indent 2 }}
{{- end -}}

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



{{- define "hull.metadata.annotations.hash" -}}
{{- $debug := false -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ $podContext := . | deepCopy }}
{{ $podContext = set $podContext "KEEP_HASHSUM_ANNOTATIONS" true }}
{{ $pod := (include "hull.object.pod" $podContext) | fromYaml }}
{{ $configmaps := dict }}
{{ $secrets := dict }}
{{ $annotations := dict }}
{{ range $container := default list (concat (dig "spec" "initContainers" list $pod) (dig "spec" "containers" list $pod)) }}
  {{ range $mount := dig "volumeMounts" list $container }}
    {{ range $volume := dig "spec" "volumes" list $pod }}
      {{ if (or (hasKey $volume "secret") (hasKey $volume "configMap")) }}
        {{ if (and (eq $volume.name $mount.name) (dig "hashsumAnnotation" false $mount)) }}
          {{ if hasKey $mount "subPath" }}
            {{ if (hasKey $volume "secret") }}
              {{ $secrets = merge $secrets (dict $volume.secret.secretName (dict $mount.subPath "")) }}
            {{ else }}
              {{ $configmaps = merge $configmaps (dict $volume.configMap.name (dict $mount.subPath "")) }}
            {{ end }}
          {{ else }}
            {{ if (hasKey $volume "secret") }}
              {{ $secrets = merge $secrets (dict $volume.secret.secretName (dict "_ALL_" "")) }}
            {{ else }}
              {{ $configmaps = merge $configmaps (dict $volume.configMap.name (dict "_ALL_" "")) }}
            {{ end }}
          {{ end }}  
        {{ end }}
      {{ end }}
    {{ end }}
  {{ end }}
  {{ range $env := dig "env" list $container }}
    {{ if dig "valueFrom" "configMapKeyRef" "hashsumAnnotation" false $env }}      
      {{ $refKey := $env.valueFrom.configMapKeyRef }}
      {{ $configmaps = merge $configmaps (dict $refKey.name (dict $refKey.key "")) }}
    {{ end }}
    {{ if dig "valueFrom" "secretKeyRef" "hashsumAnnotation" false $env }}
      {{ $refKey := $env.valueFrom.secretKeyRef }}
      {{ $secrets = merge $secrets (dict $refKey.name (dict $refKey.key "")) }}            
    {{ end }}
  {{ end }}
  {{ range $envFrom := dig "envFrom" list $container }}
    {{ if dig "configMapRef" "hashsumAnnotation" false $envFrom }}
      {{ $configmaps = merge $configmaps (dict $envFrom.configMapRef.name (dict "_ALL_" "")) }}            
    {{ end }}
    {{ if dig "secretRef" "hashsumAnnotation" false $envFrom }}
      {{ $secrets = merge $secrets (dict $envFrom.secretRef.name (dict "_ALL_" "")) }}            
    {{ end }}
  {{ end }}
{{ end }}
{{ range $type,$dict := dict "secret" $secrets "configmap" $configmaps }}
  {{ range $key, $spec := index (index $parent.Values $hullRootKey).objects $type }}
    {{ $fullName := include "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "COMPONENT" $key) }}
    {{ if (hasKey $dict $fullName) }}
      {{ $objectSpec := include (printf "hull.object.%s" $type) (dict "PARENT_CONTEXT" $parent "SPEC" $spec "OBJECT_TYPE" $type "COMPONENT" $key) | fromYaml }}
      {{ if (hasKey (index $dict $objectSpec.metadata.name) "_ALL_") }}
        {{ range $dataKey,$dataValue := $objectSpec.data }}
          {{ $annotations = merge $annotations (dict (printf "%s/%s" (printf "hashsum.%s.%s" $type $objectSpec.metadata.name | trunc 253) ($dataKey | trunc 63)) (sha256sum $dataValue)) }}
        {{ end }}
      {{ else }}
        {{ range $dataKey,$dataValue := (index $dict $objectSpec.metadata.name) }}
          {{ $annotations = merge $annotations (dict (printf "%s/%s" (printf "hashsum.%s.%s" $type $objectSpec.metadata.name | trunc 253) ($dataKey | trunc 63)) (sha256sum (index $objectSpec.data $dataKey))) }}  
        {{ end }}
      {{ end }}        
    {{ end }}          
  {{ end }}      
{{ end }}
{{ toYaml $annotations }}
{{- end -}}