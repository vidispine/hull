# Using and creating Transformations

Helm itself has by design no support for templating within the `values.yaml`. The `values.yaml` itself must be valid YAML and must not contain templating expressions. HULL can overcome this limitation to a certain degree and put templating into `values.yaml` fields.

As a simple example, it is often efficient to at least have possibilities to simply cross-reference fields in the `values.yaml`. One way this can be achieved is by using YAML anchors, the downside here is that an anchor and the reference to it need to be in the same YAML file. Considering that one main feature of Helm is to allow merging of multiple `values.yaml`'s on top of each other this approach is very limited in scope.

The HULL library provides mechanism to work around this and provide this possibility. The mechanism for this is called transformations and is extensible for even way more complex tasks by allowing to inject complex Go Templating expressions in property values of the `values.yaml`. 

## Technical Background

Technically the objects defined in the `values.yaml` are preprocessed before they are converted to Kubernetes objects. In the first internal step, Helm merges all fields of all `values.yaml`'s involved into a single YAML structure. This YAML tree is then processed key-by-key by HULL and at this stage it becomes possible to modify the YAML to the desired result by adding special keys and values to the YAML sections. When a transformation is detected during the `values.yaml` preprocessing by HULL an associated Go Templating function is called and the result replaces the transformation instruction in the resulting YAML.

⚠️ It is important to consider the fact that when a dictionary is traversed in Go Templating it is done in an alphanumeric fashion. So in order to reference the resolved value of an transformation succesfully it must have a lower alphanumeric key in the dictionary hierarchy, meaning it must have been processed first. However, since typically you would want to resolve a global value for configuration of your `hull.objects` properties in multiple places you should put your referenced value in the `hull.config.specific` section and then you can access it anytime when creating the objects. When you keep the alphanumeric processing order in mind it is furthermore no problem to use transformations on `hull.config.specific` properties too and later have the transformation result referenced by a transformation in the `hull.objects` section.⚠️

The HULL library provides transformations for all needs which can be used out of the box. It is possible to process inline Go templating expressions (see `_HT!`) and call arbitrary functions via Helms include (see `_HT/`). Additional convenience transformations are provided for easily cross-referencing values in the `values.yaml` (see `_HT*`), evaualating boolean conditions (see `_HT?`) or create chart specific object instance names (see `_HT^`). All of HULLs transformations will be explained in detail in this documentation file.

## Object Support

Currently transformations are supported for basically any input type. You can use transformations to modify property values which are:

- of string type
- of integer type
- of boolean type
- dictionaries
- arrays

⚠️ **Triggering transformations is based on the detection of a starting prefix `_HT` in key names (for dictionary values) or property values. It is not 100% guaranteed that a chart does not contain exactly this prefix pattern as a key or start of a value but otherwise it is highly unlikely.** ⚠️

## Transformation variants

This section will first highlight a simple transformation example and highlight the differences between specifying transformations in string, dictionary or array form. 


### Specyfing transformation in string form

The general syntax for any string transformation is the concatenation of three parts:

- `_HT`: 

  Prefix indicating that a transformation is defined here. All string transformations must start with this prefix.
  
  AFter this prefix comes the signalling characters defining which transformation to call.

- `<TYPE>`: 

  The type of the transformation. This is a set of defined combinations of characters with either one or two characters.

  Possible single character transformation type signals are `*`, `?`, `!`, `/`, `^` and `&`:

  - `*`: `hull.util.transformation.get`
  - `?`: `hull.util.transformation.bool`
  - `!`: `hull.util.transformation.tpl`
  - `/`: `hull.util.transformation.include`
  - `^`: `hull.util.transformation.makefullname`
  - `&`: `hull.util.transformation.selector`

  Besides this set of essential transformations, some enhanced  combinations exist which further help in writing compact configuration code:

  - `?/`: `hull.util.transformation.bool` + `hull.util.transformation.include`
  - `!*`: `hull.util.transformation.tpl` + `hull.util.transformation.get`

  The functionality and usage of all types of transformations are covered later in this document. 

- `<ARGUMENT>`

  Argument is specific to the type of the `_HT` transformation. Different transformations have a different argument structure which will be explained in more detail.

#### Example of a simple string transformation 

One simple and useful transformations is likely cross-referencing the value of a dedicated YAML field in several places in the `values.yaml` itself. As mentioned the YAML anchor approach is limited in usability so this is how you can do it using the `hull.util.transformation.get` transformation. 

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

and the output will be:

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

As shown above, the final rendered output has the transformations successfully applied. How does this work under the hood?

When key-by-key preprocessing in HULL takes place, a string starting with the prefix `_HT` is signaling that this value is being dynamically derived by calling a transformation function. The `*` sets the type to the `hull.util.transformation.get` transformation function and the remainder of `hull.config.specific.globalRegistry` is the argument specific to the `hull.util.transformation.get` transformation (a dot seperated path to the referenced field).

### Specifying transformations in form of a dictionary

A dictionary-form transformation is a transformation which is defined in form of a dictionary. It usually produces a dictionary result when it is applied. Dictionary transformations are not required usually to transform dictionaries or create them in the result. The same can be achieved with less typing by putting in a `_HT` string-based definition of the transformation instead of a dictionary. 

However, the dictionary form still does have a very potent usability for combining existing dictionary entries with dynamically generated ones in those scenarios when the JSON schema requires values to be dictionaries themselves. This is mostly the case when HULL represents Kubernetes arrays as dictionaries with a key and dictionary value structure such as in the case of e.g. `volumeMounts`. This is best demonstrated with an example.


#### Example of a dictionary transformation 

If you want to execute a dictionary transformation, you specify `_HT` plus the single transformation specific character (`*`, `?`, `!`,`^` or `&`) as a key in the dictionary. As the value to this key, again a dictionary with a single key is expected whose name can be chosen freely (suggestion is `_`) and the actual argument value for that keys value is the argument to the transformation:

```yaml
some_object_key_with_a_dictionary_value: 
  _HT!:
    _: <CONTENT of the tpl transformation>
```

Let us assume you have a container in a pod-based object defined in your helm chart and this container is supposed to always have some standard `volumeMounts`, for example a `configmap` volumeMount for application configuration. However, for certificate handling it may be required to file-mount a dynamic number of certificate files into the pod using `subPath`. A `volumeMounts` section which both has defined static entries and dynamic entries could look like this:

```yaml
volumeMounts:
  configmap: # a static volumeMount, always present unless set to enabled: false
    name: configmap
    mountPath: 'app/config/appsettings.json'
    subPath: appsettings.json
    hashsumAnnotation: true
  _HT: 
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

Given that there are any certificates to be mounted found, in the result the `volumeMounts` are populated with entries for `configmap` and `etcssl` and a single entry for each certificate.As highlighted, the dictionary transformation definition style is a powerful tool to combine static dictionary entries with dynamically created ones when the schema demands the property value to be a dictionary itself.  


## Available HULL transformations

The following transformations are provided by HULL. Especially given the reusability of the `_HT/` include and the flexibility of the `_HT!` tpl transformations they should cover all usecases. The `_HT/` transformation basically opens the door to integrating additional reusable Helm `functions` while `_HT!` is the swiss-army knife to perform special operations in-place. Nevertheless the remaining transformations are also efficient tools in the transformation kit to save time and effort in writing chart definitions. 

Here is the full list of transformations:

### `_HT*`: Get a value (_hull.util.transformation.get_)

#### __Argument__ 

The referenced key within `values.yaml` to get the value from in dot notation. Per default, the key path needs to be specified starting from `.Values` only, for exampe `hull.config.specific.value_to_get`. There are further argument tweaks available as explained below.

##### Accessing non-`hull` scoped values

To access non-`hull` scoped values, the double asterisk may be used instead of a single asterisk (`_HT**`). This effecrtively sets the start of search path to the root context instead of `$.hull` and provides access to subchart values or Helm in-built properties. 

##### Escaping dots in key names within the dotted path

Note that if any path element itself contains a dot (`.`) you can escape it with the `§` character to still be able to reference it, for example if you want to reference the key path:

  ```yaml
  hull:
    config:
        specific:
          'key.with.dots.in.it': hello dots!
  ```

you can do so by using the HULL get transformation like this:

`_HT*hull.config.specific.key§with§dots§in§it`

##### Self referencing object type and object instance key

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

#### __Produces__

The value of the referenced key within `values.yaml`. 

#### __Description__

Provides an easy to use shortcut to simply get the value of a field in `values.yaml`. This is supported for referenced values of simple types (string, integer or boolean). Getting array and dictionary values as they are is also supported, if these complex structures should be serialized you can refer to the list of allowed serialization prefixes below.

⚠️ **In case the referenced value should be manipulated in any other way you can use `_HT!` transformations in combination with the `_HT*` reference style. For more information see the 'Example of a complex custom transformation' above and the `hull.util.transformation.tpl` section below** ⚠️

When used in the `values.yaml` context, any complex object (dictionary or array) referenced will in fact be inserted as an object with further leafes into the `values.yaml` tree. This is very powerful since it allows to reuse larger configuration parts multiple times. But in some cases you may want to serialize the referenced dictionary or list object into a JSON or YAML string, for this you have the additional possibility to prefix the REFERENCE with one of the following prefixes:

- `toJson`
- `toPrettyJson`
- `toRawJson`
- `toYaml`
- `toString`
- `none`

to produce a formatted string in the output instead of an object. You need to seperate the serialization prefix with a `|` to seperate it from the original REFERENCE in this case. For example, the following are regular usages of `_HT*`:

```
_HT*hull.config.specific.some_string
_HT*hull.config.specific.some_dictionary
```

and may for example resolve to this:

```
some_string: "this was a string value defined at hull.config.specific.some_string"
some_dictionary: 
  a:
    tree:
      like: structure
```

If you want to use the serialization function to produce a JSON string for example, use this syntax:

```
_HT*toJson|hull.config.specific.some_string
_HT*toJson|hull.config.specific.some_dictionary
```

and you get a serialized string for `some_dictionary` (the `some_string` remains unchanged when serialized to JSON):

```
some_string: "this was a string value defined at hull.config.specific.some_string"
some_dictionary: '{"a": {"tree": {"like": "structure" }}}'
```

Contexts where this serialization comes in handy is when when writing configuration JSON to `annotations` or `env` vars. In the context of ConfigMaps and Secrets this is also usable but there exists a more configurable approach explained in the respective document.

For more complex get operations use the `hull.util.transformation.tpl` transformation to format or process the result before returning it.

#### __Short Form Examples__

```yaml
string: _HT*hull.config.specific.string_value_to_get
int: _HT*hull.config.specific.int_value_to_get
dictionary: _HT*hull.config.specific.dictionary_value_to_get
serialized_dictionary: _HT*toJson:hull.config.specific.dictionary_value_to_get
```

### __Get Chart/Release informations__

If you want to access root informations in your Chart you need to provide an additional `*` to change the context.

```yaml
release-name: _HT**Release.Name
chart-name: _HT**Chart.Name
```

### Create dynamic fullname (_hull.util.transformation.makefullname_)

#### __Arguments__

- COMPONENT: 
  
  The static component name

#### __Produces__

The processed fullname, typically `<CHART_NAME>_<RELEASE_NAME>_<COMPONENT>`

#### __Description__

Resembles the typically used helper function to create a unique object name per type by inlcuding chart and instance names.

#### __Short Form Examples__

```yaml
string: _HT^component-name
```

### Render a string with `tpl` (_hull.util.transformation.tpl_)

#### __Arguments__

- CONTENT: 

  The string that might contain templating expressions

#### __Produces__

The processed result of executing `tpl` on the string. Depending on where this transformation is used this can be a dictionary, a string or an array of strings.

#### __Description__

The most powerful transformation that allows to freely specify the Go templating expression(s) to be evaluated. Care needs to be taken so that the returned string can be converted to the desired return type if it is not string.

Consider using the `_HT*` reference style within the `_HT!` content to address fields in the `values.yaml` for more compact style and less typing. The full range of `_HT*` usage is available, hence you can also use `_HT**` for root context access or serialization instructions as in `_HT*toJson|hull.config.xyz`.

#### __Combinations__

`_HT!*`: 

Using this short form, which represents a combination of the `hull.util.transformation.tpl` and `hull.util.transformation.get` functionality, is the fastest way to write a `tpl` based transformation on a single field value. Technically, using this short form will simply wrap the following content with double curly opening and closing braces automatically. This means you should use it only when you want to process an operation that is containable within one templating expression statement - which is intended to include a `values.yaml` field access in this case for usefulness. Instead of a `_HT*` transformation, which prevents fully flexible processing of the rererenced fields value, the full Helm templating toolset can be applied to manipulate a field value. With the possibility to apply `_HT*`-style syntax in `_HT!` content it is very close to using `_HT*` in terms of effort but offers all processing options naturally.

This is an example where it makes sense to resort to `_HT!*` transformations.

Instead of writing:

```yaml
string: _HT!{{ (index . "$").Values.hull.config.specific.some_referenced_value | lower }}
```

or more concisely:

```yaml
string: _HT!{{ _HT*hull.config.specific.some_referenced_value | lower }}
```

you may use the most concise form:

```yaml
string: _HT!*_HT*hull.config.specific.some_referenced_value | lower
```

All three variants yield the same result. 


#### __Short Form Examples__

```yaml
# regular values.yaml access
string: _HT!{{ printf "%s-%s" (index . "$").Values.hull.config.specific.
  prefix_value_to_get (index . "$").Values.hull.config.specific.
  suffix_value_to_get }}

# _HT* reference style
string: _HT!{{ printf "%s-%s" _HT*hull.config.specific.
  prefix_value_to_get _HT*hull.config.specific.
  suffix_value_to_get }}

array: # array-form transformation style
- _HT!
    [ 
      {{ (index . "$").Values.hull.config.specific.prefix_value_to_get }}, 
      {{ (index . "$").Values.hull.config.specific.suffix_value_to_get }}
    ]

ports: # dictionary-form transformation style
  _HT!:
    "_": |-
      {
         first: { containerPort: {{ _HT*hull.config.specific.port_one }} },
         second: { containerPort: {{ _HT*hull.config.specific.port_two }} }
      }
```

### Call an `include` function (_hull.util.transformation.include_)

#### __Arguments__

- CONTENT: 

  The input to the `include` call consists of the `include`'s name first and trailing key/value pairs consisting of arguments (key-value pairs). All input fields are separated by `:`, in case of a `:` present in an argument you can use the replacement character `§` in the input which will be converted to `:` when processed. 

  The `include` name, which is the first element in the CONTENT array after splitting it with `:`, has an optional `key reference` value which is detected in case the `include` name argument is split with `/`. If a `/` is present in the `include` name, the part before `/` denotes the key to get the values from in case a dictionary is produced by the `include` function call. The second part after the `/` marks the `include` name.

  Analogously to `_HT*` you can use the following prefixes:

  - `toJson`
  - `toPrettyJson`
  - `toRawJson`
  - `toYaml`
  - `toString`

  before a `:` to serialize the result of the `_HT/` to one of the string formats.

  To facilitate easy use with HULL `include`s, the key value pair `"PARENT_CONTEXT" (index . "$")` is automatically added to the arguments dictionary in case the key `PARENT_CONTEXT` is not explicitly supplied. 

  Key names are automatically quoted so no quotes are to be provided for key names, string values however require quoting (see `hull.metadata.name` example below).

#### __Produces__

The `include` functions result of calling it with the provided arguments. 

#### __Description__

While calling an `include` function can also be realized with the _hull.util.transformation.tpl_ transformation and an `include` instruction in the argument, this transformation shortens the required input to the most compressed form. 

As an example, consider using the `hull.metadata.chartref` `include` from `_templates/metadata_chartref.yaml` as a _hull.util.transformation.tpl_ transformation and a _hull.util.transformation.include_ transformation. The `hull.metadata.chartref` `include` returns a string:

```yaml
chartref_tpl: _HT!{{ include "hull.metadata.chartref" (dict "PARENT_CONTEXT" (index . "$")) }}
chartref_include: _HT/hull.metadata.chartref
```

This is an example with additional parameters, a call to `hull.metadata.name`, also returning a string:

```yaml
name_tpl: _HT!{{ include "hull.metadata.name" (dict "PARENT_CONTEXT" (index . "$") "COMPONENT" "test") }}
name_include: _HT/hull.metadata.name:COMPONENT:"test"
```

⚠️ **In case the referenced value should be manipulated in any other way you can use `_HT!` transformations in combination with the `_HT/` include style! For more information see the 'Example of a complex custom transformation' above and the `hull.util.transformation.tpl` section below** ⚠️

Hence the following:

```yaml
name_include_in_tpl: _HT!{{ _HT/hull.metadata.name/COMPONENT:"test" }}
name_include: _HT/hull.metadata.name:COMPONENT:"test"
```

also delivers identical results while the `name_include_in_tpl` expression provides the possibility to further manipulate the returned value.

It is possible to not only return simple strings but also complex dictionaries or arrays produced by the `include`. Without an extra serialization prefix the resulting object tree or list is inserted into the `values.yaml`.

In case of an expected YAML dictionary, you can optionally denote a dictionary key in the result to get the key's values from and insert them instead of the dictionaries root key itself. If no optional dictionary key is provided, the complete dictionary returned is the result. The following example will expand on this feature and explain the difference.

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

Since the goal of this example is to replace the objects `labels` key's value with the actual labels (and not a dictionary which itself has a `labels` root entry) you must use the optional key reference feature to just pick the dictionary values from the returned `labels` dictionary under the `labels` key to return them.

So while this _hull.util.transformation.include_:

```yaml
hull:
  objects:
    configmap:
      component-name:
        labels: _HT/labels/hull.metadata.labels:COMPONENT:"overwritten-component-name"
```

will produce the expected result:

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

using the _hull.util.transformation.include_ without the key reference to `labels`:

```yaml
hull:
  objects:
    configmap:
      component-name:
        labels: _HT/hull.metadata.labels:COMPONENT:"overwritten-component-name"
```

will produce an unwanted result with doubled `labels` key:

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

#### __Short Form Examples__

```yaml
chartref_include: _HT/hull.metadata.chartref
name_include: _HT/hull.metadata.name:COMPONENT:"test"
labels: _HT/labels/hull.metadata.labels:COMPONENT:"overwritten-component-name"
dictionary_include: _HT/custom.function.returning.dictionary
yaml_serialized_dictionary_include: _HT/toYaml:custom.function.returning.dictionary
json_serialized_dictionary_include: _HT/toJson:custom.function.returning.dictionary

```

### Evaluate a condition to a boolean with `tpl` (_hull.util.transformation.bool_)

#### __Arguments__

- CONDITION: 

  The string that contains the literal condition to be checked against

#### __Produces__

A boolean return value that can be used to populate a boolean field. There is no need to supply outer `{{` and `}}` templating signs because the CONDITITION is already assumed to be within these curly braces to save typing.

#### __Description__

Typical use of this function is to set the `enabled` field on objects depending on a particular condition. Internally it uses `tpl` to produce a boolean result from the evaluation of the literal CONDITION.

The `enabled` fields explicitly allow string as an input which makes them subjectable to this transformation returning the boolean result.

#### __Combinations__

`_HT?/`: 

The combination of the `hull.util.transformation.bool` with the `hull.util.transformation.include` is an effective way to workaround the problem that in Helm Go templating it is not possible to return a boolean (or any other type besides string) from an `include` call. This leads to the problem, that even if an `include` returns literal `true` or `false` it is treated as a string which - if subject of an boolean condition check  always yields `true`. 

Assume an `include` function named `hull.test.bool` which produces `true` or `false`. If used with a `_HT/` include:

```yaml
bool-test: _HT/hull.test.bool
```

the value of `bool-test` will always be `true`. However, if paired with the conditional check via `_HT?` the actualy result will be of boolean type representing the boolean interpretation of `true` and `false`:

```yaml
bool-test: _HT?/hull.test.bool
```


#### __Short Form Examples__

```yaml
bool_field: _HT?and 
  (index . "$").Values.hull.config.specific.switch_one_enabled (index .
  "$").Values.hull.config.specific.switch_two_enabled
```

### Create a dictionary with `selector` labels for a given name (_hull.util.transformation.selector_)

#### __Arguments__

- COMPONENT: 

  The string that contains the name of the component to create selector dictionary for

#### __Produces__

A dictionary return value that can be used to populate a `selector` field.

#### __Description__

Typical use of this function is to set the `matchLabels` field on a `networkpolicy`'s `podSelector`. By using this transformation the `matchLabels` will automatically be inline with the default HULL `selector` labels.

#### __Short Form Examples__

```yaml
podSelector:
  matchLabels: _HT&mycomponentname
```

## Example of a complex custom transformation

The HULL library comes with the predefined `hull.util.transformation.tpl` transformation (short form: `_HT!`) which adds a crucial functionality to HULL rendered string and object values. Is was already used in the previous examples. 

While the principal HULL concept is to provide full control over all object values to the creators and consumers directly it might be required to still wrap logic decisions in the creation of some string, dictionary or string array values. A very typical example might be the arguments to a containers command which could depend on custom application specific fields the user should be able to define. It can be argued that this adds in a functionality that is the most basic in the regular helm workflow. In HULL this should be used with care but allows more flexibility for some HULL rendered objects that would otherwise be missing.

So in short, this transformation puts the templating back into the calculation of values. Consider the following HULL configuration: 

```yaml
hull:
  config:
    specific: # Here you can put all that is particular configuration for your app
      if_this_arg_is_defined: --this-is-defined # Whenever this is not empty ...
      then_add_this_arg: --hence-is-this # also add this argument
      
      if_this_arg_is_not_defined:  # Whenever this is empty ...
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
              args: |-
                _HT![
                  {{ if (index . "$").Values.hull.config.specific.if_this_arg_is_defined }}
                    "{{ (index . "$").Values.hull.config.specific.if_this_arg_is_defined }}",
                    "{{ (index . "$").Values.hull.config.specific.then_add_this_arg }}",
                  {{ end }}
                  {{ if not (index . "$").Values.hull.config.specific.if_this_arg_is_not_defined }}
                    "{{ (index . "$").Values.hull.config.specific.then_use_this_arg }}"
                  {{ end }}
                ]
```

The intention of the above configuration is to demonstrate some conditional population of the `args` array. It should result in three elements:

```yaml
- --this-is-defined # always as value of specific key if_this_arg_is_defined
- --hence-is-this # value of key then_add_this_arg should be added when key this-is-defined has a value
- --and-this-because-other-is-not-defined # value of key then_use_this_arg should be added when key if_this_arg_is_not_defined is not defined
```
On rendering the following happens:

- for `args` the transformation `hull.util.transformation.tpl` is executed on the string array via its short form `_HT!` and string transformation notation. 
- the `CONTENT` argument is subjected to the `tpl` Go Templating function. This renders string input with potential placeholders. 

  > Note that the `"`s need to be escaped with `\"` if the CONTENT value is surrounded with `"`'s.  

  Following additional rules apply to the usage of templating expressions in this manner:

  - when referring to the `.Values` in `values.yaml` you need to refer to 

    ```yaml
    (index . "$").Values
    ```

    instead. This is because the parent charts context is being passed into the `tpl` function as a dictionary parameter `$`. Nevertheless full access to all fields of the `values.yaml` is possible.
    
    ⚠️ **Instead of `(index . "$")` you can alternatively use the longer legacy form `(index . "PARENT")` which is slight longer to write but does the same.** ⚠️

    The key `(index . "$")` is not the only special context variable you can use directly. When you execute a transformation in the scope of an objects definition (somewhere beneath `hull.objects.<object_type>.<object_instance_key>`) you have direct access to the objects type and object instance key as string values by accessing `(index . "OBJECT_TYPE")` and `(index . "OBJECT_INSTANCE_KEY")`. This is helpful because otherwise you would need to pass in the information manually each time if you want to use it in your transformation for naming purposes for example.

    To exemplify this, if you use these settings:

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

  - When the `tpl`-ed string should result in a string array, use the 

    ```yaml
    ["value1","value2"] 
    ```

    [flow style](https://dev.to/javanibble/yaml-essentials-520b) notation to produce the resulting string array. This overcomes typical indentation pitfalls with the block style:

    ```yaml
    - value1
    - value2
    ```
    
    notation. 
    
    The same holds for returned dictionaries as well, the `tpl`'ed result needs to be composed in flow style syntax like in this example:
    
    ```yaml
    { 
      key_one: { inner_string: "value1", inner_int: 1 }, 
      key_two: { inner_string: "value2", inner_int: 2 }
    }
    ```

The rendered result again contains the intended `args` section:

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
        env: []
        envFrom: []
        image: my/image/repo:99.9
        name: main
        ports: []
        volumeMounts: []
      initContainers: []
      serviceAccountName: release-name-hull-test-default
      volumes: []
```

Alternatively, HULL also allows to define field references in the `_HT!` content in the same syntax which is defined for the `_HT*` transformations (explained below). This provides an even more concise way of providing field references within the `tpl` content. The following specification is equivalent to the one already given:

```yaml
hull:
  config:
    specific: # Here you can put all that is particular configuration for your app
      if_this_arg_is_defined: --this-is-defined # Whenever this is not empty ...
      then_add_this_arg: --hence-is-this # also add this argument
      
      if_this_arg_is_not_defined:  # Whenever this is empty ...
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

Additionally the `include` short form transformation `_HT/` is now also available for use within `_HT!` content! To correctly delimit the `_HT/` parameters from the remaining `_HT!` content, it needs to be ended with a `/TH_` suffix, similar to a bash `if`/`fi` start/end tag. 

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

More detailed on this feature is available in the below section on _hull.util.transformation.tpl_ transformations.

---
Back to [README.md](./../README.md)