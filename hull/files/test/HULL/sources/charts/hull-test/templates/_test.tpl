{{- define "hull.include.test.imagepullsecrets.emptyarray" -}}
[]
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptyarray" -}}
- name: "a"
- name: "b"
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.emptyflow" -}}
[]
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptyflow" -}}
[
  { "name": "flowa" },
  { "name": "flowb" }
]
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.emptylist" -}}
{{  list | toYaml }}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.nonemptylist" -}}
{{ list (dict "name" "listreg1") (dict "name" "listreg2") | toYaml }}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.emptyarray" -}}
result: []
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.nonemptyarray" -}}
result:
- name: "a"
- name: "b"
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.emptyflow" -}}
{ 
  "result": []
}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.nonemptyflow" -}}
{ 
  "result": [
    { "name": "flowa" },
    { "name": "flowb" }
  ]
}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.emptylist" -}}
{{ dict "result" list | toYaml }}
{{- end -}}

{{- define "hull.include.test.imagepullsecrets.indirect.nonemptylist" -}}
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

{{- define "hull.include.test.true" -}}
true
{{- end -}}

{{- define "hull.include.test.false" -}}
false
{{- end -}}

{{- define "hull.include.test.true.string" -}}
"true"
{{- end -}}

{{- define "hull.include.test.false.string" -}}
"false"
{{- end -}}

{{- define "hull.include.test.true.from.field" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $parent.Values.hull.config.specific.env_bool_true -}}
{{- end -}}

{{- define "hull.include.test.false.from.field" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $parent.Values.hull.config.specific.env_bool_false -}}
{{- end -}}
