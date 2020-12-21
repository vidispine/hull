{{- /*
| Purpose:  
|   
|   Create a volume: reference in a pod specification
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.object.volume" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $component := default "" (index . "COMPONENT") -}}
{{- $spec := default nil (index . "SPEC") -}}
- {{ dict "name" $component | toYaml }}
{{- if hasKey $spec "configMap" }}   
{{ include "hull.object.volume.configmap" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec.configMap) | indent 2 }}
{{- else -}}
{{- if hasKey $spec "secret" }}   
{{ include "hull.object.volume.secret" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec.secret) | indent 2 }}
{{- else -}}
{{ if hasKey $spec "persistentVolumeClaim" }}   
{{ include "hull.object.volume.persistentVolumeClaim" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "SPEC" $spec.persistentVolumeClaim) | indent 2 }}
{{- else -}}
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "configMap" "secret" "persistentVolumeClaim")) | indent 2 }}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Create a ConfigMap volume
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.volume.configmap" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
configMap:
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "name")) | indent 2 }}
  name: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.name "SPEC" $spec) }}
{{ end -}}



{{- /*
| Purpose:  
|   
|   Create a Secret volume
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.volume.secret" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
secret:
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "secretName")) | indent 2 }}
  secretName: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.secretName "SPEC" $spec) }}
{{ end -}}



{{- /*
| Purpose:  
|   
|   Create a PersistentVolumeClaim volume
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   SPEC: The dictionary to work with
|
*/ -}}
{{- define "hull.object.volume.persistentVolumeClaim" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $spec := default nil (index . "SPEC") -}}
persistentVolumeClaim: 
{{ include "hull.util.include.k8s" (dict "PARENT_CONTEXT" $parent "SPEC" $spec "HULL_OBJECT_KEYS" (list "claimName")) | indent 2 }}
  claimName: {{ template "hull.metadata.fullname" (dict "PARENT_CONTEXT" $parent "COMPONENT" $spec.claimName "SPEC" $spec) }}
{{ end -}}