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

{{- define "hull.include.test.dockerconfigjson" -}}
{{ $reg := dict "my-registry" (dict "username" "username" "password" "password" "email" "email" "auth" "dXNlcm5hbWU6cGFzc3dvcmQ=") }}
{{ $auths := dict "auths" $reg }}
{{ printf "%s" ($auths | toPrettyJson) }}
{{- end -}}