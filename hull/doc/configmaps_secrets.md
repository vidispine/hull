# Creating ConfigMaps and Secrets

ConfigMaps and Secrets can be created very efficient using the HULL library. The actual contents can be either defined inline in the `values.yaml` for shorter contents or sourced via an external file.

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
          a_configmap_data_instance:
            inlines:
              inline_1:
                data: |-
                  Concrete Inline 1
            files:
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