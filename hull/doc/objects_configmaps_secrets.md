# Creating ConfigMaps and Secrets

ConfigMaps and Secrets can be created very efficient using the HULL library. The actual contents can be either defined inline in the `values.yaml` for shorter contents or sourced via an external file.

## JSON Schema Elements

### The `hull.VirtualFolder.v1` properties


| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`data:`&#160; | Dictionary with Key-Value pairs. Can be used to specify ConfigMap or Secret data sourced from inline specification or external files.<br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.VirtualFolderData.v1`** properties. See below for reference. | `{}` | `settings.json:`<br>&#160;&#160;`path:`&#160;`'files/settings.json'`<br>`application.config:`<br>&#160;&#160;`path:`&#160;`'files/appconfig.yaml'`<br>&#160;&#160;`noTemplating: true`<br>`readme.txt:`<br>&#160;&#160;`inline:`&#160;`'Just`&#160;`a`&#160;`text'`

### The `hull.VirtualFolderData.v1` properties

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `inline` | The actual data specified inline in the `values.yaml` to store in the ConfigMap or Secret. <br><br>Note: If set, the `path` and `noTemplating` properties are ignored. | | `'Just`&#160;`a`&#160;`text'`
| `path` | An external file path to read contents from. Path must be relative to the charts root path.<br> Files can contain templating expressions which are rendered by default, this can be disabled by setting `noTemplating: true`.<br><br>Note: If `inline` property is set, the `path` and `noTemplating` properties are ignored. | | `'files/settings.json'`
| `noTemplating` | If `noTemplating` is specified and set to `true`, no templating expressions are rendered when the content is processed. <br>This can be useful in case you need to handle text content already containing Go or Jinja templating expressions which should not be handled by Helm but by the deployed application.<br>If `noTemplating: false` or the key `noTemplating` is missing, templating expressions will be processed by Helm when importing the content.<br><br>Note: If `inline` property is set, the `path` property is ignored. | `false`| `true`

## Examples
First off, define any ConfigMap or Secret under the `hull.objects` `configmap` or `secret` key by giving them a unique key name within the respective object type.

Consider the following two files in the parent Helm charts `/files` folder:

file_1.json:
```json
{
  "name": "i am file_1.json"
}
```

file_2.yaml:
```yaml
name: "i am file_2.yaml"
templating: "{{ .Values.hull.config.general.metadata.labels.custom.label_1 }}"
```

See the following example:

```yaml

hull:
  config:
    general:
      metadata:
        labels:
          custom:
            label_1: foo
  objects:
    configmap:
      a_configmap:
        data:          
          inline_1:
            inline: |-
              Concrete Inline 1
          file_1.json:
            path: files/file_1.json
          file_2_templated.yaml:
            path: files/file_2.yaml
            noTemplating: false
          file_2.yaml:
            path: files/file_2.yaml
            noTemplating: true
```

This will create a ConfigMap with the following data section:

```yaml
data:
  inline_1: Concrete Inline 1
  file_1.json: |-
    {
      "name": "i am file_1.json"
    }
  file_2_templated.yaml: |-
    name: "i am file_2.yaml"
    templating: foo
  file_2.yaml: |-
    name: "i am file_2.yaml"
    templating: "{{ .Values.hull.config.general.metadata.labels.custom.label_1 }}"
```

It is furthermore possible to combine the [transformation](./transformations.md) functionality with the templating of external files. This means you can dynamically calculate a field in the `values.yaml` via a transformation and then reference the result in the ConfigMap or Secret. 

Here is an example showcasing this feature. See the following example:

```yaml
hull:  
  config:
    specific: # Here you can put all that is particular configuration for your app
      value_to_resolve_1: trans 
      value_to_resolve_2: formation
      resolve_me: "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.tpl>>><<<CONTENT=
        {{ printf \"%s%s\" (index . \"PARENT\").Values.hull.config.specific.value_to_resolve_1 (index . \"PARENT\").Values.hull.config.specific.value_to_resolve_2 }}
        >>>"  # Transformation to combine 'trans' and 'formation' to the word
              # 'transformation' via referencing two other fields
  objects:
    configmap:
      transformation_resolving:
        enabled: true
        staticName: false
        data:
          resolved_transformation.txt:
            path: files/resolve_transformation.txt
```

and the external file `files/resolve_transformation.txt` with contents:

```yaml
This is a text file with a pointer to a {{ .Values.hull.config.specific.resolve_me }}.
```

When processing, the transformation is applied to the contents of `values.yaml` before the result is passed to the `tpl` function processing the external file's content. In the end a ConfigMap is built with the following expected `data` property:

```yaml
data:
  resolved_transformation.txt: This is a text file with a pointer to a transformation.
```

---
Back to [README.md](./../README.md)