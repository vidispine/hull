# Creating ConfigMaps and Secrets

ConfigMaps and Secrets can be created very efficient using the HULL library. The actual contents can be either defined inline in the `values.yaml` for shorter contents or sourced via an external file. Whether the content of `data` content is specified `inline` (inside the `values.yaml`) or via a `path` (an external file) is fully transparent to HULL because internally it is implemented in the same way. Equally, it does not make a difference whether you are specifying Secret or ConfigMap `data`, the HULL interface for specification is identical for both. The only difference is that HULL automatically takes care of the Base64 encoding of values for Secrets so you don't need to. See the examples section below for more details on usage possibilities.

## JSON Schema Elements

### The `hull.VirtualFolder.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `binaryData:`&#160; | Dictionary with Key-Value pairs. Can be used to specify binary data sourced from external files.<br><br>Key: <br>Unique related to parent element and not matching any key in `data`.<br><br>Value: <br>The **`hull.BinaryData.v1`** properties. See below for reference. | `{}` | `binaryfile.bin:`<br>&#160;&#160;`path:`&#160;`'files/binaryfile.bin'` |
| `data:`&#160; | Dictionary with Key-Value pairs. Can be used to specify ConfigMap or Secret data sourced from inline specification or external files.<br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.VirtualFolderData.v1`** properties. See below for reference. | `{}` | `settings.json:`<br>&#160;&#160;`path:`&#160;`'files/settings.json'`<br>`application.config:`<br>&#160;&#160;`path:`&#160;`'files/appconfig.yaml'`<br>&#160;&#160;`noTemplating: true`<br>`readme.txt:`<br>&#160;&#160;`inline:`&#160;`'Just`&#160;`a`&#160;`text'` |

### The `hull.BinaryData.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair defined as `path` will be rendered for deployment. If resolved to false, it will be omitted. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | `true`<br>`false`<br><br>`_HT?hull.config.specific.enable_addon` |
| `path` | An external file path to read binary contents from. Path must be relative to the charts root path. | | `'files/binaryfile.bin'` |

### The `hull.VirtualFolderData.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair defined as ``inline` or via `path` will be rendered for deployment. If resolved to false, it will be omitted. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | `true`<br>`false`<br><br>`_HT?hull.config.specific.enable_addon` |
| `inline` | The actual data specified inline in the `values.yaml` to store in the ConfigMap or Secret. <br><br>Note: If set, the `path` and `noTemplating` properties are ignored. | | `'Just`&#160;`a`&#160;`text'` |
| `path` | An external file path to read contents from. Path must be relative to the charts root path.<br> Files can contain templating expressions which are rendered by default, this can be disabled by setting `noTemplating: true`.<br><br>Note: If `inline` property is set, the `path` and `noTemplating` properties are ignored. | | `'files/settings.json'` |
| `noTemplating` | If `noTemplating` is specified and set to `true`, no templating expressions are rendered when the content is processed. <br>This can be useful in case you need to handle text content already containing Go or Jinja templating expressions which should not be handled by Helm but by the deployed application.<br>If `noTemplating: false` or the key `noTemplating` is missing, templating expressions will be processed by Helm when importing the content.<br><br>Note: If `inline` property is set, the `path` property is ignored. | `false` | `true` |
| `serialization` | If `serialization` is specified it needs to have one of the following values: `toJson`, `toPrettyJson`, `toRawJson`, `toYaml`, `toString` or `none`. <br>With this explicit serialization command you can force the content of the `data` entry to be serialized in one of the formats. <br><br>Normally only `toJson`, `toPrettyJson`, `toRawJson` and `toYaml` are practical options for serializing any object. <br><br>Note that `toString` will produce an internal object representation when used on dictionaries and lists which is normally undesired. Setting `none` skips any serialization actions and is equivalent to not specifying the `serialization` key. | | `toJson`<br>`toPrettyJson`<br>`toRawJson`<br>`toYaml`<br>`toString`<br>`none` |
| `preEncoded` | If `preEncoded` is specified and set to `true`, no Base64 encoding is performed when content from `inline` or `path` is processed. This mandates that the source content is already Base64 encoded. <br>This can be useful in case you want to import pre-Base64-encoded binary data into a secret in order to mount it into a pod as a binary file.<br>If `preEncoded: false` or the key `preEncoded` is missing, as demanded by Kubernetes, Base64 encoding is automatically performed on the source content when writing it to the secret.<br><br>Note: This property only applies to Secret data fields and has no effect on ConfigMap data fields. | `false` | `true` |

## Features and Examples

First off, define any ConfigMap or Secret under the `hull.objects` `configmap` or `secret` key by giving them a unique key name within the respective object type.

### Templating

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

It is furthermore possible to combine the [transformation](./../transformations.md) functionality with the inherent templating of `data` values that HULL does (except when `noTemplating` is set). In terms of ConfigMap and Secret management, one of the original ideas for HULL was to make it as easy and "natural feeling" as possible to add content inline in values.yaml and use templating in the content. This includes the possibility to use regular templating in the content. To achieve this, in the HULL code tpl is by default always run on inline content (or on the content in an external file if using the `path` property instead). The original chart context `.` or `$` is passed to this tpl call and can be accessed directly as in regular Helm chart templates.This means you can dynamically calculate a field in the `values.yaml` via a transformation and then reference the result in the ConfigMap or Secret via normal templating syntax.

Here is an example showcasing this feature. See the following example:

```yaml
hull:  
  config:
    specific: # Here you can put all that is particular configuration for your app
      value_to_resolve_1: trans 
      value_to_resolve_2: formation
      resolve_me: |- 
        _HT!
          {{ 
             printf "%s%s" (index . "$").Values.hull.config.specific.value_to_resolve_1 
                           (index . "$").Values.hull.config.specific.value_to_resolve_2 
          }}
      # Transformation to combine 'trans' and 'formation' to the word
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

Furthermore you can also utilize the `_HT*` Get- and the `_HT/` Include-transformation as well to conveniently include values in your `data` which are produced in other places in your chart. This can be used to copy string input into your ConfigMap or Secret's `data` but is even more powerful when using it to serialize dictionaries or arrays.

Assume you have a dictionary whose input is to be provided at configuration time under `hull.specific.app-configuration` and the following dummy data is provided:

```yaml
hull:
  config:
    specific:
      simple-string: "This is a simple string to be written to a ConfigMap"
      app-configuration:
        some-value: "imagine some text"
        number: 333
        true-or-false: true
        subdict:
          key1: a key
          key2: another key
```

Simply put in a `_HT*` transformation into your `data` field and specify a `serialization: toYaml` for example:

```yaml
hull:
  config:
    specific:
      simple-string: "This is a simple string to be written to a ConfigMap"
      app-configuration:
        some-value: "imagine some text"
        number: 333
        true-or-false: true
        subdict:
          key1: a key
          key2: another key
  objects:
    configmap:
      app:
        data:
          simple-string:
            inline: _HT*hull.config.specific.simple-string
          app-configuration-yaml:
            serialization: toYaml
            inline: _HT*hull.config.specific.app-configuration
          app-configuration-json:
            serialization: toPrettyJson
            inline: _HT*hull.config.specific.app-configuration
```

and the result is serialized YAML, JSON and simple string:

```yaml
simple-string: This is a simple string to be written to a ConfigMap
app-configuration-yaml: |-
  number: 333
  some-value: imagine some text
  subdict:
    key1: a key
    key2: another key
  true-or-false: true
app-configuration-json: |-
  {
    "number": 333,
    "some-value": "imagine some text",
    "subdict": {
      "key1": "a key",
      "key2": "another key"
    },
    "true-or-false": true
  }
```

More on serialization in the context of ConfigMap and Secret data in the next section.

### Serialization

First of, normal `inline` content which is specified as a string or contents in a file pointed to by `path` will by default always be treated as strings and no automatic serialization will take place. This is important to by default transport the character sequences as they are to the rendered YAML.

While normally HULL expects string input to regular `data` entry values, extended support is provided for serializing to common configuration formats `YAML` and `JSON`. You can use HULL's seriallization feature by either:

- giving an explicit `serialization` instruction to a `data` entry in which case an explicit serialization of the content is done. In this case the `inline` content may be defined as a dictionary, a list or a string. The `path` contents are always treated as strings. In the case of string `inline` or `path` data, the actual content must be valid YAML or JSON after all transformations and processing of content has been done. The content may be specified in place or may even be referenced to via a `_HT*` Get- or `_HT/`-Include transformation via your `inline` or `path` contents.

- using implicit serialization by file extension. This only applies for dictionary or list content which itself again maybe specified in-place as the `inline` value or be referenced to via a `_HT*` Get- or `_HT/`-Include transformation via your `inline` or `path` contents. If the `data` key ends with `.json` the output is serialized `toPrettyJson`, for the common YAML file extensions `.yml` and `.yaml` the `toYaml` function is called.

In the following example, the same JSON content:

```yaml
{
  "this": "is",
  "an": "example",
  "to": "show"
  "a": "number",
  "of": 4,
  "serialization": "options",
}
```

is written to the ConfigMap six times under they keys:

- `no-serialization.json`: no implicit serialization is done on string content irregarding any file extension
- `implicit-from-dictionary.json`: implicitly converted from dictionary content due to `.json` file extension
- `implicit-from-get-transformation.json`: implicitly converted from referenced dictionary content due to `.json` file extension
- `explicit-from-dictionary`: explicitly converted from dictionary due to `serialization: toPrettyJson` and no `.json` file extension being set
- `explicit-from-yaml.yaml`: explicitly converted from a YAML structure given as a string due to `serialization: toPrettyJson`
- `explicit-none-conversion.json`: explicitly instructing the `serialization` to use no serializer is the same as `no-serialization.json`

```yaml
hull:
  config:
    specific:
      demo-example:
        this: is
        an: example
        to: show
        a: number
        of: 4
        serialization: options
  objects:
    configmap:
      doc-json-serialization-examples:
        data:
          no-serialization.json:
            inline: |-
              { 
                "this": "is", 
                "an": "example", 
                "to": "show", 
                "a": "number", 
                "of": 4, 
                "serialization": "options" 
              }
          implicit-from-dictionary.json:
            inline:
              this: is
              an: example
              to: show
              a: number
              of: 4
              serialization: options
          implicit-from-get-transformation.json:
            inline: _HT*hull.config.specific.demo-example
          explicit-from-dictionary:
            serialization: toPrettyJson
            inline:
              this: is
              an: example
              to: show
              a: number
              of: 4
              serialization: options
          explicit-from-yaml.yaml:
            serialization: toPrettyJson
            inline: |-
              this: is
              an: example
              to: show
              a: number
              of: 4
              serialization: options
          explicit-none-conversion.json:
            serialization: none
            inline: |-
              { 
                "this": "is", 
                "an": "example", 
                "to": "show", 
                "a": "number", 
                "of": 4, 
                "serialization": "options" 
              }
```

Note that due to the usage of Helms in-built functions for serialization the order of dictionary key-value elements is not preserved when using `toJson`, `toPrettyJson` or `toRawJson` serialization. If you need or want to preserve the order of keys in the JSON you must specify the JSON as a string. Additionally, either specify no `serialization` key or use `serialization: none` to not deserialize and serialize the data again. This is exemplified by the keys `no-serialization.json` and `explicit-none-conversion.json` which add the following key-value pairs to `data`, preserving the original order of keys:

```yaml
no-serialization.json: |-
  { 
    "this": "is", 
    "an": "example", 
    "to": "show", 
    "a": "number", 
    "of": 4, 
    "serialization": "options" 
  }
explicit-none-conversion.json: |-
  { 
    "this": "is", 
    "an": "example", 
    "to": "show", 
    "a": "number", 
    "of": 4, 
    "serialization": "options" 
  } 
```

For the other four produced `data` entries, the order of keys was not preserved and is alphanumerically rearranged as it is the standard in most serializers:

```yaml
implicit-from-dictionary.json: |-
  {
    "a": "number",
    "an": "example",
    "of": 4,
    "serialization": "options",
    "this": "is",
    "to": "show"
  }
implicit-from-get-transformation.json: |-
  {
    "a": "number",
    "an": "example",
    "of": 4,
    "serialization": "options",
    "this": "is",
    "to": "show"
  }
explicit-from-dictionary: |-
  {
    "a": "number",
    "an": "example",
    "of": 4,
    "serialization": "options",
    "this": "is",
    "to": "show"
  }
explicit-from-yaml.yaml: |-
  {
    "a": "number",
    "an": "example",
    "of": 4,
    "serialization": "options",
    "this": "is",
    "to": "show"
  }
```

If maintaing the order of elements is important you need to use raw string method of specifying your object.

---
Back to [README.md](/README.md)
