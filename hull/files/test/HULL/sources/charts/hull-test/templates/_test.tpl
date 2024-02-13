{{- define "hull.include.test.imagepullsecrets.emptyarray" -}}
result: []
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptyarray" -}}
result:
- name: "a"
- name: "b"
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.emptyflow" -}}
{ 
  "result": []
}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptyflow" -}}
{ 
  "result": [
    { "name": "flowa" },
    { "name": "flowb" }
  ]
}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.emptylist" -}}
{{ dict "result" list | toYaml }}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptylist" -}}
{{ dict "result" (list (dict "name" "listreg1") (dict "name" "listreg2")) | toYaml }}
{{- end -}}

{{- define "hull.include.test.dockerconfigjson.flow" -}}
{"auths":{"my-registry":{"username":"username","password":"password","email":"email","auth":"dXNlcm5hbWU6cGFzc3dvcmQ="}}}
{{- end -}}

{{- define "hull.include.test.dockerconfigjson.code" -}}
{{- $reg := dict "my-registry" (dict "username" "username" "password" "password" "email" "email" "auth" "dXNlcm5hbWU6cGFzc3dvcmQ=") -}}
{{- $auths := dict "auths" $reg -}}
{{- $auths | toYaml -}}
{{- end -}}

{{- define "hull.include.test.dockerconfigjson.code.quote" -}}
{{- $reg := dict "my-registry" (dict "username" "username" "password" "password" "email" "email" "auth" "dXNlcm5hbWU6cGFzc3dvcmQ=") -}}
{{- $auths := dict "auths" $reg -}}
{{- $auths | toYaml -}}
{{- end -}}

{{- define "hull.include.test.dockerconfigjson.flow.quote" -}}
'{"auths":{"my-registry":{"username":"username","password":"password","email":"email","auth":"dXNlcm5hbWU6cGFzc3dvcmQ="}}}'
{{- end -}}

{{- define "hull.include.test.volumes.postrender" -}}
{{- $instance := (index . "INSTANCE") -}}
instance:
  configMap:
    name: {{ $instance }}
{{- end -}}