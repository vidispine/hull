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
| `noTemplating` | If `noTemplating` is specified and set to `true`, no templating expressions are rendered when file content is processed. <br>This can be useful in case you need to handle files already containing Go or Jinja templating expressions which should not be handled by Helm but by the deployed application.<br>If `noTemplating: false` or the key `noTemplating` is missing, templating expressions will be processed by Helm when importing the file.<br><br>Note: This only works when importing from external files.<br><br>Note: If `inline` property is set, the `path` and `noTemplating` properties are ignored. | `false`| `true`

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
            noTemplating: true
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

---
Back to [README.md](./../README.md)