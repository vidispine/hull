# Using HULL Transformations

Helm itself has by design no support for templating within the `values.yaml`. The `values.yaml` itself must be valid YAML and must not contain templating expressions. HULL can overcome this limitation to a certain degree and put templating into `values.yaml` fields.

As a simple example, it is often efficient to at least have possibilities to simply cross-reference fields in the `values.yaml`. One way this can be achieved is by using YAML anchors, the downside here is that an anchor and the reference to it need to be in the same YAML file. Considering that one main feature of Helm is to allow merging of multiple `values.yaml`'s on top of each other this approach is very limited in scope.

The HULL library provides mechanism to work around this and provide this possibility. The mechanism for this is called transformations and is extensible for even way more complex tasks by allowing to inject complex Go Templating expressions in property values of the `values.yaml`. While the principal HULL concept is to provide full control over all object values to the creators and consumers directly it might be required to still wrap logic decisions in the creation of some string, dictionary or string array values. A very typical example might be the arguments to a containers command which could depend on custom application specific fields the user should be able to define elsewhere. 

In regular Helm, the templates provide the means to realize dependencies. In HULL, transformations put the templating back into the calculation of values.

## Technical Background

Technically, the objects defined in the `values.yaml` are preprocessed before they are converted to Kubernetes objects. In the first internal step, Helm merges all fields of all `values.yaml`'s involved into a single YAML structure. This YAML tree is then processed key-by-key by HULL and at this stage it becomes possible to modify the YAML to the desired result by adding special keys and values to the YAML sections. When a transformation is detected during the `values.yaml` preprocessing by HULL an associated Go Templating function is called and the result replaces the transformation instruction in the resulting YAML.

It is important to consider the fact that when a dictionary is traversed in Go Templating it is done in an alphanumeric fashion. So in order to reference the resolved value of an transformation succesfully it would need to have a lower alphanumeric key in the dictionary hierarchy, meaning it must have been processed first. However, since typically you would want to resolve a global value for configuration of your `hull.objects` properties in multiple places you should put your referenced value in the `hull.config.specific` section and then you can access it anytime when creating the objects. When you keep the alphanumeric processing order in mind it is furthermore no problem to use transformations on `hull.config.specific` properties too and later have the transformation result referenced by a transformation in the `hull.objects` section. Note also that the problem is leverageable to some degree by running multi-passes at HULL transformation rendering. By default, HULL will scan the YAML tree three times consecutively for HULL transformations, making it possible to use forward references via `_HT*` to later processed fields in the YAML tree that also have a HULL transformation as content. In a first pass, the literal content of a later processed key will be copied when using `_HT*` but in the second run the copied transformation will be resolved. To visualize multi-pass redndering please consider the following example:

```
hull:
  config:
    general:
      render:
        passes: 3
    specific:
      field_a: _HT*hull.config.specific.field_b
      field_b: _HT*hull.config.specific.field_c
      field_c: _HT*hull.config.specific.field_d
      field_d: _HT*hull.config.specific.field_e
      field_e: _HT*hull.config.specific.field_f
      field_f: _HT*hull.config.specific.field_g
      field_g: "Found me!"
  objects:
    deployment:
      multi-pass-test:
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-python-direct
                tag: 23.3.2
              env:
                RESOLVE_A:
                  value: _HT*hull.config.specific.field_a
```

When varying the `hull.config.general.render: 3` from 1 to 3 the value of `field_a` with its chain of forward references will get resolved in a different manner.

With `hull.config.general.render.passes: 1`, the env var `RESOLVE_A` resolves to `_HT*hull.config.specific.field_c`, the yet unresolved literal value of `field_b`.

With `hull.config.general.render.passes: 2`, the env var `RESOLVE_A` resolves to `_HT*hull.config.specific.field_g`, effectively already resolving a large number of forward references.

With `hull.config.general.render.passes: 3`, the env var `RESOLVE_A` resolves to `Found me!`, thus all forward references were resolved successfully.



The HULL library provides transformations for all needs which can be used out of the box. It is possible to process inline Go templating expressions (see `_HT!`) and call arbitrary functions via Helms include (see `_HT/`). Additional convenience transformations are provided for easily cross-referencing values in the `values.yaml` (see `_HT*`), evaualating boolean conditions (see `_HT?`) or create chart specific object instance names (see `_HT^`). All of HULLs transformations will be explained in detail in this documentation file.

## Object Support

Currently transformations are supported for basically any input type. You can use transformations to modify property values which are:

- of string type
- of integer type
- of boolean type
- dictionaries
- arrays

⚠️ **Triggering transformations is based on the detection of a starting prefix `_HT` in key names (for dictionary values) or property values. It is not 100% guaranteed that a chart does not contain exactly this prefix pattern as a key or start of a value but otherwise it is highly unlikely.** ⚠️

## Transformation definitions

This section will highlight the differences between specifying transformations in string or dictionary form.


### Specyfing transformation in string form

The general syntax for any string transformation is the concatenation of three parts:

- `_HT`: 

  Prefix indicating that a transformation is defined here. All string transformations must start with this prefix.
  
  After this prefix comes the type signalling characters defining which transformation to call.

- `<TYPE>`: 

  The type of the transformation. This is denoted by a single character.

  Allowed single character transformation type signals are `*`, `?`, `!`, `/`, `^` and `&`:

  - `*`: `hull.util.transformation.get`
  - `!`: `hull.util.transformation.tpl`
  - `/`: `hull.util.transformation.include`
  - `?`: `hull.util.transformation.bool`
  - `^`: `hull.util.transformation.makefullname`
  - `&`: `hull.util.transformation.selector`

  The functionality and usage of all types of transformations are covered later in this document. 

- `<ARGUMENT>`

  Argument is specific to the type of the `_HT` transformation. Different transformations have very different and sometimes complex argument structures  explained in more detail in the remainder of this document.

#### Example of a simple string transformation 

One simple and useful transformations is likely cross-referencing the value of a dedicated YAML field in several places in the `values.yaml` itself. As mentioned the YAML anchor approach is limited in usability so this is how you can do it using the `hull.util.transformation.get`/`_HT*` transformation. 

Assuming you have a local docker registry endpoint you want to use as the registry for several container images, you can achieve this like this:

```yaml
hull:
  config:
    specific:
      globalRegistry: local.registry # this is the value I want to 
                                     # reuse in multiple places

  objects:
    deployment:
      
      external_app:
        pod:
          containers:

            external:
              image:
                repository: quay.io/external_app
                tag: "latest"

            internal_one:
              image:
                registry: _HT*hull.config.specific.globalRegistry # here it is used
                repository: internal_app1
                tag: "latest"

            internal_two:
              image: 
                registry: _HT*hull.config.specific.globalRegistry # and here
                repository: internal_app2
                tag: "latest"
```

and the output will be similar to this:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations: {}
  labels:
    app.kubernetes.io/component: external_app
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-external_app
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: external_app
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations: {}
      labels:
        app.kubernetes.io/component: external_app
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.31.0
        helm.sh/chart: hull-test-1.31.0
   spec:
      containers:
      - image: quay.io/external_app:latest
        name: external
      - image: local.registry/internal_app1:latest
        name: internal_one
      - image: local.registry/internal_app2:latest
        name: internal_two
```

While metadata may vary of course, the `spec` contains the resolved transformations in the rendered output. How does this work under the hood?

When key-by-key preprocessing in HULL takes place, a string starting with the prefix `_HT` is signaling that this value is being dynamically derived by calling a transformation function. The `*` sets the type to the `hull.util.transformation.get` transformation function and the remainder of `hull.config.specific.globalRegistry` is the argument specific to the `hull.util.transformation.get` transformation (a dot seperated path to the referenced field). The calculated result of the `_HT*` invocation replaces the `_HT*` definition in the YAML tree and is written to the output YAML.

### Specifying transformations in form of a dictionary

A dictionary-form transformation is a transformation which is defined in form of a dictionary. It usually produces a dictionary result when it is applied. Dictionary transformations are not required usually to transform dictionaries or create them in the result. The same can be achieved with less typing by putting in a `_HT` string-based definition of the transformation instead of a dictionary. 

However, the dictionary form does have one particular usability for combining existing dictionary entries with dynamically generated ones in scenarios when the JSON schema requires property values to be dictionaries themselves. This is mostly the case when HULL represents Kubernetes arrays as dictionaries with a key and dictionary value structure such as in the case of e.g. `volumeMounts`. This is best demonstrated with an example.

#### Example of a dictionary transformation 

If you want to execute a dictionary transformation, you specify `_HT` plus the single transformation specific character (`*`, `?`, `!`,`^` or `&`) as a key in the dictionary. As the value to this key, again a dictionary with a single key is expected whose name can be chosen freely (suggestion is `_`) and the actual argument value for that keys value is the argument to the transformation:

```yaml
some_object_key_with_a_dictionary_value: 
  _HT!:
    _: <CONTENT of the tpl transformation>
```

Let us assume you have a container in a pod-based object defined in your helm chart and this container is supposed to always have some standard `volumeMounts`, for example a `configmap` volumeMount for application configuration. However, for certificate handling it may be required to file-mount a dynamic number of certificate files into the pod using `subPath`. The dynamic list of certs is provided elsewhere in your chart, here under `hull.config.general.data.installation.config.customCaCertificates`.

 A `volumeMounts` section which both has static entries and dynamic entries could be generated like this:

```yaml
volumeMounts:
  configmap: # a static volumeMount, always present unless set to enabled: false
    name: configmap
    mountPath: 'app/config/appsettings.json'
    subPath: appsettings.json
    hashsumAnnotation: true
  _HT!: 
    _: |- # iterate over a dictionary with certificate file names and contents and add one volumeMount per provided file from a volume named certs which is supposed to contain the referenced certificate files
      {
        {{ range $certkey, $certvalue := (index . "$").Values.hull.config.general.data.installation.config.customCaCertificates}}
        "custom-ca-certificates-{{ $certkey }}": 
          {
            enabled: true, 
            name: "certs",
            mountPath: "/usr/local/share/ca-certificates/custom-ca-certificates-{{ $certkey }}",
            subPath: "{{ $certkey }}",
            hashsumAnnotation: true
          },
        {{ end }}
      }
  etcssl:
    enabled: _HT?(index . "$").Values.hull.config.general.data.installation.config.customCaCertificates # this volumeMount only needs to be there if any certificate is provided
    name: etcssl
    mountPath: '/etc/ssl/certs'
```

Given that there are two certificates `test_cert_1` and `test_cert_2` to be mounted found, in the result the `volumeMounts` are populated with entries for `configmap` and `etcssl` and entries for each certificate:

```yaml
volumeMounts:
- mountPath: /usr/local/share/ca-certificates/custom-ca-certificates-test_cert_1
  name: certs
  subPath: test_cert_1
- mountPath: /usr/local/share/ca-certificates/custom-ca-certificates-test_cert_2
  name: certs
  subPath: test_cert_2
- mountPath: app/config/appsettings.json
  name: configmap
  subPath: appsettings.json
- mountPath: /etc/ssl/certs
  name: etcssl
```

As highlighted, the dictionary transformation definition style is a powerful tool to combine static dictionary entries with dynamically created ones when the schema demands the property value to be a dictionary itself.


## In-built HULL transformations

The following transformations are provided by HULL. Especially given the reusability of the `_HT/` include and the flexibility of the `_HT!` tpl transformations they should cover all usecases. The `_HT/` transformation basically opens the door to integrating additional reusable Helm `define`s while `_HT!` is the swiss-army knife to perform special operations in-place. Nevertheless the remaining transformations are also efficient tools in the transformation tool kit to save time and effort in writing chart definitions.

Here is the full list of transformations:

### `_HT*`: Get a value (_hull.util.transformation.get_)

#### __Description__

Provides an easy to use shortcut to simply get the value of a field in `values.yaml`. This is supported for referenced values of simple types (string, integer or boolean). Getting array and dictionary values as they are is also supported. When used in the `values.yaml` context, any complex object (dictionary or array) referenced will in fact be inserted as an object - protentially adding further leafs - into the `values.yaml` tree. This is very powerful since it allows to reuse larger configuration parts multiple times. In some cases you may want to serialize the referenced dictionary or list object into a JSON or YAML string which is also supported.

⚠️For more complex get operations use the `hull.util.transformation.tpl` transformation to format or fully process the result before returning it. ⚠️


#### __Produces__

The unchanged or serialized value of the referenced key within `values.yaml`. 

#### __Argument__ 

The referenced key within `values.yaml` to get the value from in dot notation. Per default, the key path needs to be specified starting from `.Values` only, for exampe `hull.config.specific.value_to_get`. There are further argument tweaks available as explained below.

##### __Accessing non-`hull` scoped values__

To access non-`hull` scoped values, the double asterisk may be used instead of a single asterisk (`_HT**`). This effecrtively sets the start of search path to the root context instead of `.hull` and provides access to subchart values or Helm in-built properties. 

To access release or chart information or another charts property use this syntax:

```yaml
release-name: _HT**Release.Name
chart-name: _HT**Chart.Name
other-charts-important-property: _HT**other-chart.important-property
```


##### __Escaping dots in key names within the dotted path__

Note that if any path element itself contains a dot (`.`) you can escape it with the `§` character to still be able to reference it, for example if you want to reference the key path:

  ```yaml
  hull:
    config:
        specific:
          'key.with.dots.in.it': hello dots!
  ```

you can do so by using the HULL get transformation like this:

`_HT*hull.config.specific.key§with§dots§in§it`

##### __Self referencing object type and object instance key__

If `_HT*` is used in a field beneath `hull.objects.<OBJECT_TYPE>.<OBJECT_INSTANCE_KEY>`, it also possible to reference the current contexts `OBJECT_TYPE` and `OBJECT_INSTANCE_KEY` via special static keys: 
  
  - `§OBJECT_TYPE§` and 
  - `§OBJECT_INSTANCE_KEY§` 
  
in the dotted path. The keys must be exactly written like this. If such a key is found in the dotted path, the replacing of `§` for `.` is of course not performed for this special value. 
  
To give an example, with this `values.yaml`:

```yaml
hull:
  config:
    specific:
      components:
        deployment:
          ht-get-object-type-example-doc: "Just some demo value to be referenced ..."
  objects:
    deployment:
      ht-get-object-type-example-doc: 
        pod:
          containers:
            main:
              image:
                repository: app-repository
                tag: "1.0"
              env:
                GET_FROM_HULL_CONFIG:
                  value: _HT*hull.config.specific.components.§OBJECT_TYPE§.§OBJECT_INSTANCE_KEY§
```
  
you get a rendered result containing:

```yaml
containers:
- env:
  - name: GET_FROM_HULL_CONFIG
    value: Just some demo value to be referenced ...
  image: app-repository:1.0
  name: main
```

To exemplify this with another example, if you use these settings:

```
hull:
  objects:
    configmap:
      test-configmap-key:
        object_instance_key:
          inline: _HT!{{ (index . "OBJECT_INSTANCE_KEY") }}
        object_type:
          inline: _HT!{{ (index . "OBJECT_TYPE") }}
```

you will render the following ConfigMap entries in the output:

```
object_instance_key: test-configmap-key
object_type: configmap
```

⚠️ **Note that if you use `(index . "OBJECT_INSTANCE_KEY")` or `(index . "OBJECT_TYPE")` outside of an object instance definition such as `hull.objects.<object_type>.<object_instance_name>` the resulting values will be empty strings.** ⚠️


##### __Serializing referenced arrays or dictionaries__

To serialize a referenced fields value, you have the additional possibility to prefix the argument with one of the following prefixes:

- `toJson`
- `toPrettyJson`
- `toRawJson`
- `toYaml`
- `toString`
- `none`

to produce a formatted string in the output instead of an object. You need to seperate the serialization prefix with a `|` to seperate it from the dotted path specification. 

For example, the following are regular usages of `_HT*`:

```
_HT*hull.config.specific.some_string
_HT*hull.config.specific.some_dictionary
_HT*hull.config.specific.some_array
```

and may for example resolve to this:

```
some_string: "this was a string value defined at hull.config.specific.some_string"
some_dictionary: 
  a:
    tree:
      like: structure
some_array:
- with
- three
- items
```

If you want to use the serialization function to produce a pretty formatted JSON string for example, use this syntax:

```
_HT*toPrettyJson|hull.config.specific.some_string
_HT*toPrettyJson|hull.config.specific.some_dictionary
_HT*toPrettyJson|hull.config.specific.some_array
```

and you get nice and pretty serialized string representations for `some_dictionary` and `some_array` (the `some_string` remains unchanged when serialized to JSON):

```
some_string: "this was a string value defined at hull.config.specific.some_string"
some_dictionary: |-
  {
    "a": {
      "tree": {
        "like": "structure" 
      }
    }
  }
some_array: |-
  [
    "with",
    "three",
    "items"
  ]
```

Contexts where this serialization comes in handy is when when writing configuration JSON to `annotations` or `env` vars. In the context of ConfigMaps and Secrets this is also usable but there exists a more more convenient serialization approaches explained in the respective document for ConfigMaps and Secrets.

⚠️Serialization of transformation results is also possible for `_HT/` and `_HT!` transformations!⚠️

If you want to serialize data from a non-`hull` context, you can combine serialization and root context access like this: 

```yaml
serialized_dictionary_from_other_context: _HT**toPrettyJson|other-chart.dictionary-to-serialize
```

where the double `**` comes before the serialization instruction.

#### __Examples__

```yaml
string: _HT*hull.config.specific.string_value_to_get
int: _HT*hull.config.specific.int_value_to_get
dictionary: _HT*hull.config.specific.dictionary_value_to_get
serialized_dictionary: _HT*toYaml|hull.config.specific.dictionary_to_serialize
serialized_dictionary_from_other_context: _HT**toPrettyJson|other-chart.dictionary-to-serialize
```


### `_HT/`: Call an `include` function (_hull.util.transformation.include_)

#### __Description__

This transformation is a shortcut to call any `define` function via Helms `include` command. While calling an `include` function can also be realized with the `_HT!` transformation and an `include` instruction in the argument, this transformation shortens the required input to the most compressed form. 

As an example, consider using the `hull.metadata.chartref` `include` from `_templates/metadaa_chartref.yaml` as a `_HT!` transformation and a `_HT/` transformation. The `hull.metadata.chartref` `include` returns a string:

```yaml
chartref_tpl: _HT!{{ include "hull.metadata.chartref" (dict "$" (index . "$")) }}
chartref_include: _HT/hull.metadata.chartref
```

While both calls are equivalent, the `_HT!` call requires additional syntax that can be easily omitted when the goal is to call exactly one `define`. 

This is an example with additional parameters, a call to `hull.metadata.name`, also returning a string:

```yaml
name_tpl: _HT!{{ include "hull.metadata.name" (dict "PARENT_CONTEXT" (index . "$") "COMPONENT" "test") }}
name_include: _HT/hull.metadata.name:COMPONENT:"test"
```

For dictionaries and arrays, without an extra serialization prefix the resulting object tree or list is inserted into the `values.yaml` tree.

⚠️ **In case the returned value should be manipulated in any other way you can use `_HT!` transformations in combination with an embedded `_HT/` include style! For more information see the `_HT!_` section below** ⚠️


#### __Produces__

The `include` functions result of calling it with the provided optional parameters in the argument. 

#### __Argument__

The most basic input to the `include` call consists simply of the `include`'s name. 

##### Passing arguments to the `include` call

To pass any number of key-value parameters to the include call, trailing key/value pairs consisting of additional parameters may be added. The following rules must apply:

- all parameter key and value fields are separated by `:` from each other. 
- key names are automatically quoted so no quotes need to be provided for key names
- string values require quoting (see `hull.metadata.name` example above). 
- within the values, access to the root context is made by using `(index . "$")`.


##### __Escaping colons in include argument values__

In case of a `:` present in an argument value, you can use the replacement character `§` in the input which will be converted to `:` when processed. 

##### __Retrieving value of a particular key in a dictionary results__ 

In case of an expected YAML dictionary, you can optionally denote a dictionary key in the result to get the key's values from and insert them instead of the dictionaries root key itself. If a `/` is present in the `include` name (that is before any `:` starting the argument key-value pairs), the part before `/` denotes the key to get the values from in case a dictionary is produced by the `include` function call. The second part after the `/` marks the `include` name. If no optional dictionary key is provided, the complete dictionary returned is the result. The following example will expand on this feature.

Assume you want to call an _hull.util.transformation.include_ transformation on an objects `labels` section to overwrite the `app.kubernetes.io/component` label value `component-name`.  with the provided COMPONENT value `overwritten_component_name`. Under the hood the `hull.metadata.labels` `include` is called internally to create the complete standard `labels` block automatically. By making another explicitly call to this `include` with a different component name we can effectively overwrite the `app.kubernetes.io/component` label value. Note that normally you'd not want to overwrite the standard labels, this is just for demonstration purposes! 

The `hull.metadata.labels` `include` is the `include` that produces the labels block looks like this:

```yaml
{{- /*
| Purpose:  
|   
|   Write combined labels: block from custom and default annotations
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   PARENT_TEMPLATE: Metadata for the template section
|   COMPONENT: The instance name to be used in creating names
|
*/ -}}
{{- define "hull.metadata.labels" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $template := (index . "PARENT_TEMPLATE") -}}
{{- $component := (index . "COMPONENT") -}}
{{- $hullRootKey := default "hull" (index . "HULL_ROOT_KEY") -}}
{{ $labels := dict }}
{{ $labels = merge $labels (include "hull.metadata.labels.custom" . | fromYaml) }}
{{ $labels = merge $labels ((include "hull.metadata.general.labels.object" .) | fromYaml) }}
{{ if (gt (len (keys (index (index $parent.Values $hullRootKey).config.general.metadata.labels "custom"))) 0) }}
{{ $labels = merge $labels (index $parent.Values $hullRootKey).config.general.metadata.labels.custom }}
{{- end -}}
{{ $labels = merge $labels ((include "hull.metadata.labels.selector" (dict "PARENT_CONTEXT" $parent "COMPONENT" $component "HULL_ROOT_KEY" $hullRootKey)) | fromYaml) }}
{{ if default false (index . "MERGE_TEMPLATE_METADATA") }}
{{ $labels = merge $labels ((include "hull.metadata.labels.custom" (merge (dict "LABELS_METADATA" "templateLabels") . ) | fromYaml)) }}
{{- end -}}
labels:
{{ toYaml $labels | indent 2 }}
{{- end -}}
```

and you see that the returned YAML dictionary itself contains the root key `labels`. 

Since the goal of this example is to replace the objects `labels` key's value with the actual labels (and not a dictionary which itself has a `labels` root entry) you can use the optional key reference feature to just pick the dictionary values from the returned `labels` dictionary under the `labels` key to return them.

So while this _hull.util.transformation.include_ `_HT/` call including the `labels` reference:

```yaml
hull:
  objects:
    configmap:
      component-name:
        labels: _HT/labels/hull.metadata.labels:COMPONENT:"overwritten-component-name"
```

will produce the expected `metadata` result block in the ConfigMap `component-name`:

```yaml
...
metadata:
  labels:
    app.kubernetes.io/component: overwritten-component-name
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
...
```

Using the _hull.util.transformation.include_ without the key reference to `labels`:

```yaml
hull:
  objects:
    configmap:
      component-name:
        labels: _HT/hull.metadata.labels:COMPONENT:"overwritten-component-name"
```

will produce an unwanted result with a doubled `labels` key:

```yaml
...
metadata:
  labels:
    labels:
      app.kubernetes.io/component: overwritten-component-name
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/managed-by: Helm
      app.kubernetes.io/name: hull-test
      app.kubernetes.io/part-of: undefined
      app.kubernetes.io/version: 1.31.0
...
```

##### __Serializing referenced arrays or dictionaries__

Analogously to `_HT*` you can use the following prefixes:

  - `toJson`
  - `toPrettyJson`
  - `toRawJson`
  - `toYaml`
  - `toString`

to serialize the result of the `_HT/` to one of the string formats.

If used in combination with __retrieving value of a particular key in a dictionary results__, the serialization instruction needs to prepend the `key` name (`result` in this example):

```yaml
_HT/toJson|result/hull.include.test.imagepullsecrets.indirect.nonemptylist
```

#### __Examples__

```yaml
chartref_include: _HT/hull.metadata.chartref
name_include: _HT/hull.metadata.name:COMPONENT:"test"
labels: _HT/labels/hull.metadata.labels:COMPONENT:"overwritten-component-name"
dictionary_include: _HT/custom.function.returning.dictionary
yaml_serialized_dictionary_include: _HT/toYaml|custom.function.returning.dictionary
json_serialized_dictionary_include: _HT/toJson|custom.function.returning.dictionary

```


### `_HT!`: Render a string with `tpl` (_hull.util.transformation.tpl_)

#### __Description__

The powerful in-place transformation that allows to freely specify the Go templating expression(s) to be evaluated. Care needs to be taken so that the returned string can be converted to the desired return type.

#### __Produces__

The processed result of executing `tpl` on the string. Depending on where this transformation is used this can be a an object of any type.

#### __Argument__

A string that is subjected to `tpl` command. By intention the string likely contains templating expressions to be resolved on `tpl` execution, otherwise a regular string would suffice as input. 

⚠️The string definition must be interpretable successfully by `tpl`, otherwise it may result in an empty string output or an error raised by HULL.⚠️

##### __Returning dictionaries or array from `_HT!`__

When the `tpl`-ed string should result in an array, for example a string array, it is required to use the 

```yaml
[
  "value1","value2"
] 
```

[flow style](https://dev.to/javanibble/yaml-essentials-520b) notation to produce the resulting string array. This overcomes typical indentation pitfalls with the block style:

```yaml
- value1
- value2
```

notation such as indentation and whitespace chomping.

⚠️It is required to use flow-style in the tpl argument when specifying dictionaries or arrays for best compatibility!⚠️

The same holds for returned dictionaries as well, the `tpl`'ed result must be composed in flow style syntax like in this example:

```yaml
{ 
  key_one: { inner_string: "value1", inner_int: 1 }, 
  key_two: { inner_string: "value2", inner_int: 2 }
}
```

##### __Serializing referenced arrays or dictionaries__

Analogously to `_HT*` and `_HT/` you can use the following prefixes:

  - `toJson`
  - `toPrettyJson`
  - `toRawJson`
  - `toYaml`
  - `toString`

to serialize the result of the `_HT!` to one of the string formats.

##### Embedding HULL transformation syntax `_HT*` and `_HT/` in  the `_HT!` argument

Due to a special preprocessing of the `_HT!` argument, it is possible to use the `_HT*` and `_HT/` syntax within the `_HT!` argument instead of the regular Go templating ways to achieve the same result. This allows concise combinations of the convenience transformations with the flexible `_HT!` transformation.

Putting a `_HT*` into a `_HT!` argument is straightforward since the `_HT*` transformation by design does not allow whitespaces in the argument and is easily detectable:

```yaml
value: |-
  _HT!
    {{- printf "The value of key hull.config.specific.demo-value is %s" _HT*hull.config.specific.demo-value -}}
```

The full range of `_HT*` usage is available, hence you can also use `_HT**` for root context access or serialization instructions as in `_HT*toJson|hull.config.xyz`.

To correctly delimit the `_HT/` parameters - potentially containing whitespace - from the remaining `_HT!` content, they need to be ended with a `/TH_` suffix, similar to a bash `if`/`fi` start/end tag. 

Here is a brief example on how to put `_HT/` transformations into the `_HT!` content:

```yaml
value: |-
  _HT!
    {{- printf "%s is the chart reference value" _HT/hull.
    metadata.chartref/TH_ -}}
```

This will render similar to the below, depending on your parents helm charts name and version:

```yaml
value: hull-test-1.31.0 is the chart reference value
```

In the same vein, the following two calls:

```yaml
name_include_in_tpl: _HT!{{ _HT/hull.metadata.name/COMPONENT:"test"/TH_ }}
name_include: _HT/hull.metadata.name:COMPONENT:"test"
```

deliver identical results while the `name_include_in_tpl` expression provides the possibility to further manipulate the returned value.


##### Shortcut syntax to executing a single templating command

Adding a `*` directly after the `_HT!` denotes a special variant of the `_HT!` transformation. Using prefix `_HT!*` is the fastest way to write a `tpl` based transformation on a single tempating expression that would normally be surrounded with `{{` and `}}`. Technically, using this prefix combination will simply auto-wrap the subsequent content with double curly opening and closing braces automatically. This means you should use it only when you want to process an operation that is containable within one templating expression statement. 

A typical example would be a simple modification of a referenced value. A `_HT*` transformation prevents fully flexible processing of the rererenced fields value and only allows retrieval as-is. The full Helm templating toolset can be applied to manipulate a field value during retrieval with `_HT!` however and combined with the `_HT!*` prefix this is done with minimal typing. 

With the possibility to apply `_HT*`-style syntax in `_HT!` content it is very close to using `_HT*` in terms of writing effort but offers all processing options still.

This is an example where it makes sense to resort to `_HT!*` transformations. Instead of writing:

```yaml
string: _HT!{{ (index . "$").Values.hull.config.specific.some_referenced_value | lower }}
```

or more concisely using embedded `_HT*`:

```yaml
string: _HT!{{ _HT*hull.config.specific.some_referenced_value | lower }}
```

you may trim it even further down using the most concise form:

```yaml
string: _HT!*_HT*hull.config.specific.some_referenced_value | lower
```

All three variants yield the same result. 

#### __Examples__

```yaml
# regular values.yaml access
string: _HT!{{ printf "%s-%s" (index . "$").Values.hull.config.specific.
  prefix_value_to_get (index . "$").Values.hull.config.specific.
  suffix_value_to_get }}

# _HT* reference style
string: _HT!{{ printf "%s-%s" _HT*hull.config.specific.
  prefix_value_to_get _HT*hull.config.specific.
  suffix_value_to_get }}

ports: # dictionary-form transformation style
  _HT!:
    "_": |-
      {
         first: { containerPort: {{ _HT*hull.config.specific.port_one }} },
         second: { containerPort: {{ _HT*hull.config.specific.port_two }} }
      }
```


### `_HT?`: Evaluate a condition to a boolean with `tpl` (_hull.util.transformation.bool_)

#### __Description__

Typical use of this function is to set the `enabled` field on objects depending on a particular condition. Internally it uses `tpl` to produce a boolean result from the evaluation of the literal argument.

The `enabled` fields explicitly allow string as an input which makes them subjectable to this transformation returning the boolean result.

#### __Produces__

A boolean return value that can be used to populate a boolean field. There is no need to supply outer `{{` and `}}` templating signs because the CONDITITION is already assumed to be within these curly braces to save typing.

#### __Argument__

The string that contains the literal condition to be checked against

##### Evaluating `_HT/` include as a boolean condition within `_HT?`

The combination of the `_HT?` with the `_HT/` in form of `_HT?/` is an effective way to workaround the problem that in Helm Go templating it is not possible to return a boolean (or any other type besides string) from an `include` call. This leads to the problem, that even if an `include` returns literal `true` or `false` it is treated as a string which - if subject of an boolean condition check always yields `true`. 

Assume an `include` function named `hull.test.bool` which produces `true` or `false` as rendered string. If used with a regular `_HT/` include:

```yaml
bool-test-incorrect: _HT/hull.test.bool
```

the value of `bool-test` will always be `true`. However, if paired with the conditional check via `_HT?` the actualy result will be of boolean type representing the boolean interpretation of `true` and `false`:

```yaml
bool-test-correct: _HT?/hull.test.bool
```


#### __Examples__

```yaml
bool_field_regular_syntax: _HT?and 
  (index . "$").Values.hull.config.specific.switch_one_enabled (index .
  "$").Values.hull.config.specific.switch_two_enabled
bool_field_hull_syntax: _HT?and 
  _HT*hull.config.specific.switch_one_enabled _HT*hull.config.specific.switch_two_enabled
```


### `_HT^`: Create dynamic fullname (_hull.util.transformation.makefullname_)

#### __Description__

Resembles the typically used helper function to create a unique object name per type by including chart and instance names.

The actual result is influenced by the properties:

```yaml
hull:
  config:
    general:  
      fullnameOverride: ""
      nameOverride: ""
```

The `_HT^` function is helpful in places where you want to refer to a chart created object instance whose name is determined at configuration time and is based on above settings. 

#### __Produces__

The processed fullname, typically `<CHART_NAME>_<RELEASE_NAME>_<COMPONENT>`

#### __Argument__

The static component name part

#### __Examples__

```yaml
string: _HT^component-name # by default produces `<CHART_NAME>-<RELEASE_NAME>-component-name`
```


### `_HT&`: Create a dictionary with `selector` labels for a given name (_hull.util.transformation.selector_)

### __Description__

Typical use of this function is to set the `matchLabels` field on a `networkpolicy`'s `podSelector`. By using this transformation the `matchLabels` will automatically be inline with the default HULL `selector` labels auto-created by HULL as well.

#### __Argument__

The string that contains the name of the component to create selector dictionary for

#### __Produces__

A dictionary return value that can be used to populate a `selector` field.

#### __Examples__

```yaml
podSelector:
  matchLabels: _HT&mycomponentname
```


## Example of a complex transformation application

Consider the following HULL configuration: 

```yaml
hull:
  config:
    specific: # Here you can put all that is particular configuration for your app
      if_this_arg_is_defined: --this-is-defined # Whenever this is not empty ...
      then_add_this_arg: --hence-is-this # also add this argument
      
      if_this_arg_is_not_defined: null # Whenever this is empty ...
      then_use_this_arg: --and-this-because-other-is-not-defined # also add this argument

  objects:
    deployment:
      custom-args:
        pod:
          containers:
            main:
              image:
                repository: my/image/repo
                tag: "99.9"
              args: _HT![
                  {{ if _HT*hull.config.specific.if_this_arg_is_defined }}
                    "{{ _HT*hull.config.specific.if_this_arg_is_defined }}",
                    "{{ _HT*hull.config.specific.then_add_this_arg }}",
                  {{ end }}
                  {{ if not _HT*hull.config.specific.if_this_arg_is_not_defined }}
                    "{{ _HT*hull.config.specific.then_use_this_arg }}"
                  {{ end }}
                ]
```
Technically, note that we are already using some special features such as embedded HULL transformations in above specification. 

Functionally, the intention of the above configuration is to demonstrate some conditional population of an `args` array. It should result in three elements:

```yaml
- --this-is-defined # always as value of specific key if_this_arg_is_defined
- --hence-is-this # value of key then_add_this_arg should be added when key this-is-defined has a value
- --and-this-because-other-is-not-defined # value of key then_use_this_arg should be added when key if_this_arg_is_not_defined is not defined
```

On rendering the following happens:

- for `args` the transformation `_HT!` internally calling include `hull.util.transformation.tpl` is executed on the string array via the usual string transformation notation. 

- the `_HT!` argument is subjected to the `tpl` Go Templating function. This renders string input with potential placeholders. 


Based on the explanations given in this document, the rendered result contains the intended `args` section:

```yaml
# Source: hull-test/templates/hull.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: custom-args
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-custom-args
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: custom-args
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      labels:
        app.kubernetes.io/component: custom-args
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.31.0
    spec:
      containers:
      - args:
        - --this-is-defined
        - --hence-is-this
        - --and-this-because-other-is-not-defined
        image: my/image/repo:99.9
        name: main
      serviceAccountName: release-name-hull-test-default
```

---
Back to [README.md](./../README.md)