{{- /*
| Purpose:  
|   
|   Gets the contents of a file by its path
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   PATH: The path to the file relative to charts root
|
*/ -}}
{{- define "hull.util.tools.file.get" -}}
{{- $path := (index . "PATH") -}}
{{ (index . "PARENT_CONTEXT").Files.Get $path }}
{{- end -}}



{{- /*
| Purpose:  
|   
|   Import multiple files into a virtualfolder based object (ConfigMap or Secret)
    by selecting them via a glob. 
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   GLOB: The glob expression to select the files
|   NOTEMPLATING: Don't template content of all imported files
|   SERIALIZATION: Apply serialization instruction to all imported files
|
*/ -}}
{{- define "hull.util.tools.virtualdata.data.glob" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $glob := (index . "GLOB") -}}
{{- $noTemplating := default false (index . "NOTEMPLATING") -}}
{{- $serialization := default "" (index . "SERIALIZATION") -}}
{
  {{ range $path, $_ := (index . "PARENT_CONTEXT").Files.Glob $glob }}
  {{ (base $path) }}: {
    'path': {{ $path }},
    'noTemplating': {{ $noTemplating }},
    {{ if (ne $serialization "") }}
    'serialization': {{ $serialization }}
    {{ end }}
  },
  {{ end }}
}
{{- end -}}