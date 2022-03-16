# Using and creating Transformations

Helm itself has by design no support for templating within the `values.yaml`. The `values.yaml` itself must be valid YAML and must not contain templating expressions. HULL can overcome this limitation to a certain degree and put templating into `values.yaml` fields.

As a simple example, it is often efficient to at least have possibilities to simply cross-reference fields in the `values.yaml`. One way this can be achieved is by using YAML anchors, the downside here is that an anchor and the reference to it need to be in the same YAML file. Considering that one main feature of Helm is to allow merging of multiple `values.yaml`'s on top of each other this approach is very limited in scope.

The HULL library provides mechanism to work around this and provide this possibility. The mechanism for this is called transformations and is extensible for even way more complex tasks by allowing to inject complex Go Templating expressions in property values of the `values.yaml`. 

## Technical Background

Technically the objects defined in the `values.yaml` are preprocessed before they are converted to Kubernetes objects. In the first internal step, Helm merges all fields of all `values.yaml`'s involved into a single YAML structure. This YAML tree is then processed key-by-key by HULL and at this stage it becomes possible to modify the YAML to the desired result by adding special keys and values to the YAML sections. When a transformation is detected during the `values.yaml` preprocessing by HULL an associated Go Templating function is called and the result replaces the transformation instruction in the resulting YAML.

⚠️ It is important to consider the fact that when a dictionary is traversed in Go Templating it is done in an alphanumeric fashion. So in order to reference the resolved value of an transformation succesfully it must be have a lower alphanumeric key in the dictionary hierarchy, meaning it must have been processed first. However, since typically you would want to resolve a global value for configuration of your `hull.objects` properties in multiple places you should put your referenced value in the `hull.config.specific` section and then you can access it anytime when creating the objects. When you keep the alphanumeric processing order in mind it is furthermore no problem to use transformations on `hull.config.specific` properties too and later have the transformation result referenced by a transformation in the `hull.objects` section.⚠️

Some transformations are part of the HULL library and can be used out of the box. It is also possible to create your own Go Templating function/transformation and use them where possible. For this you need only add a `tpl` file to your chart and define a transformation that adheres to the structural rules highlighted next.

## Object Support

Currently transformations are supported for basically any input type. You can use transformations to modify all:

- values which are of string type
- values which are of integer type
- values which are of boolean type
- values which are dictionaries
- values which are arrays

⚠️ **Triggering transformations is based on the detection of a starting prefix __\_HULL_TRANSFORMATION\___ or __\_HT__ for built-in transformation short forms in key names (for dictionary values) or string values so it is not 100% guaranteed that a chart does not use this expression as a key or value but otherwise it is highly unlikely.** ⚠️

## Transformations

This section will highlight a simple transformation example and one showcasing the full possibilities of this approach.

### Example of a simple string transformation 

One simple and  useful transformations is likely cross-referencing the value of a dedicated YAML field in several places in the `values.yaml` itself. As mentioned the YAML anchor approach is limited in usability so this is how you can do it using the `hull.util.transformation.get` transformation. 

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
                registry: "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.get>>><<<REFERENCE=hull.config.specific.globalRegistry>>>" # here it is used
                repository: internal_app1
                tag: "latest"

            internal_two:
              image: 
                registry: _HT*hull.config.specific.globalRegistry # and here
                repository: internal_app2
                tag: "latest"
```

Now when preprocessing in HULL takes place, the string starting with the key word `_HULL_TRANSFORMATION_` (or a short form starting with `_HT`) is signaling that this value is being dynamically derived by calling a transformation function. The two expressions above are now taken apart to call the transformations with named arguments.

#### String transformation interface

The general syntax for any string transformation is:

- `_HULL_TRANSFORMATION_`: 

  Prefix indicating that a transformation is defined here. All string transformations must start with this prefix (unless the short form is used).
  
  All arguments to a transformation are wrapped in `<<<ARGUMENT-NAME=ARGUMENT-VALUE>>>`

- `<<<NAME=hull.util.transformation.get>>>`: 

  The name of the transformation (the Go Template Function) to call. This is the only mandatory argument to each HULL transformation which is the first argument in the argument list. Here it is the `hull.util.transformation.get` transformation being executed.

- `<<<REFERENCE=hull.config.specific.globalRegistry>>>`

  This argument is specific to the `hull.util.transformation.get` transformation. Here it references the key from which we want to get the value from in dot-notation.

⚠️ **Note that the arguments themselves cannot contain the start-of and end-of argument signifiers `<<<` and `>>>` when using the long form syntax for transformations! These are important for string-splitting the arguments to the transformation.** ⚠️

#### Transformation short forms

As HULL comes with a predefined set of handy transformations and always typing down the regular transformation interface structure described above is inconvenient, there exist so-called __short forms__ to these four built-in transformations. The short forms take advantage of the fact that all four built-in transformations only demand a single argument so the transformation call can be done with much less typing.

In the above example we used the short form for the `hull.util.transformation.get` transformation like this: 

```yaml
registry: _HT*hull.config.specific.globalRegistry # and here
```

which is equivalent to writing:

```yaml
registry: "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.get>>><<<REFERENCE=hull.config.specific.globalRegistry>>>"
```

but much shorter. The full transformation call is reduced to a short prefix (`_HT`), a character indicating the specific transformation to use (`*` for `hull.util.transformation.get`) and the single arguments (`REFERENCE`) value without the need to specify the arguments name. The other possible characters for short forms are `?`, `!`,`^` and `&`  the following transformation short forms are available for use:

- `_HT*`: `hull.util.transformation.get`
- `_HT?`: `hull.util.transformation.bool`
- `_HT!`: `hull.util.transformation.tpl`
- `_HT^`: `hull.util.transformation.makefullname`
- `_HT&`: `hull.util.transformation.selector`

See the overview on the transformations that HULL delivers out-of-the-box for details on short form transformation syntax.

#### Example definition of a transformation

Now we can take a look at the [transformation definition] for `hull.util.transformation.get` (./../templates/_util_transformations.tpl) itself:

```yaml
{{- /*
| Purpose:
|
|   Gets the value from a key in values.yaml given dot-notation.
|
| Interface:
|
|   PARENT_CONTEXT: The Parent charts context
|   REFERENCE: The key in dot-notation for which the value should be retrieved
|
*/ -}}
{{- define "hull.util.transformation.get" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $key := (index . "KEY") -}}
{{- $reference := (index . "REFERENCE") -}}
{{- $path := splitList "." $reference -}}
{{- $current := $parent.Values }}
{{- range $pathElement := $path -}}
{{- $current = (index $current $pathElement) }}
{{- end -}}
{{- if and (typeIs "string" $current) (not $current) }}
{{ $key }}: ""
{{- else -}}
{{ $key }}: {{ (include "hull.util.transformation.convert" (dict "SOURCE" $current "KEY" $key)) }}
{{- end -}}
{{- end -}}

```

In the code above the value of the dot-notated key is retrieved via iteration over the path's elements. Then it is either returned as an empty string (if non existent) or further processed with the `hull.util.transformation.convert` function which creates the return value based on `$current` type. It is capable of returning simple types (string, bool and integer values) but also complex types including nested dictionaries and arrays.

It is mandatory for all transformations to return result data as a yaml block containing the passed in `$key` variable as key:

```yaml
{{ $key }}: "<RESULT OF TRANSFORMATION>"
```

In the source YAML the dictionary value of key `$key` is now replaced by the transformations result before rendering. Note that the type of the result field does not have to be a string but it must validate against the Kubernetes API objects JSON schema. 

⚠️⚠️⚠️ **In many scenarios the input and output types are identical so you would use a string transformation to produce a string as result. However (by now) HULL has full support to supply a string transformation instead of a boolean, integer, array or dictionary input value in `values.yaml` properties - even if the original Kubernetes schema demands the input value to be boolean, integer, array or object respectively. In this case it is the responsibility of the configurator to make sure that the transformation returns an object of the correct input type and structure otherwise Kubernetes will not accept invalid objects upon deployment time. Technically the ability to use HULL string transformations everywhere is achieved by extension of the Kubernetes JSON schema to always allow a regex conforming 'transformation' string input besides the original type of the value. Currently the regex of allowed string input is `^\s*(_HT[\*|\?|\^|!]|_HULL_TRANSFORMATION_<<<).*`. By having this ability the dictionary and array form of the HULL transformations become deprecated even though they are still usable** ⚠️⚠️⚠️

The final rendered output has the transformations successfully applied:

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
    app.kubernetes.io/version: 1.20.0
    helm.sh/chart: hull-test-1.20.1
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
        app.kubernetes.io/version: 1.20.0
        helm.sh/chart: hull-test-1.20.1
   spec:
      containers:
      - env: []
        envFrom: []
        image: quay.io/external_app:latest
        name: external
        ports: []
        volumeMounts: []
      - env: []
        envFrom: []
        image: local.registry/internal_app1:latest
        name: internal_one
        ports: []
        volumeMounts: []
      - env: []
        envFrom: []
        image: local.registry/internal_app2:latest
        name: internal_two
        ports: []
        volumeMounts: []
```

### Example of a dictionary transformation (⚠️ deprecated ⚠️)

**It is not required anymore to use a dictionary transformation to process a dictionary in HULL with a transformation. By now HULL string transformations are available for objects of all input types. Hence this feature is deprecated as of now even though still functional.** 

Input type validation might demand an `object` as a values object type. Similar to the string transformation presented above you can then also trigger a transformation by providing a dictionary as input. In this case provide the following dictionary value to the key you wish to process:

```yaml
some_object_key_with_a_dictionary_value: 
  _HULL_TRANSFORMATION_:
    NAME: "TRANSFORMATION_NAME"
    ARGUMENT1: "..."
    ARGUMENT2: "..."
    ...
```

The presence of the single `_HULL_TRANSFORMATION_` key as the value of the input object triggers the transformation. Instead of string-splitting arguments they are derived by the keys in the `_HULL_TRANSFORMATION_` dictionary.

If you use an available short form for a transformation you specify `_HT` plus the single transformation specific character (`*`, `?`, `!`,`^` or `&`) as the key. A single key is expected in the dictionary whose name can be chosen freely (suggestion is `_`) and the actual argument value for that keys value is the argument. For example, the structure presented above would look like this for the short form of the `hull.util.transformation.tpl` transformation:

```yaml
some_object_key_with_a_dictionary_value: 
  _HT!:
    "_": <CONTENT of the tpl transformation>
```

### Example of an array transformation (⚠️ deprecated ⚠️)

**It is not required anymore to use an array transformation to process a dictionary in HULL with a transformation. By now HULL string transformations are available for objects of all input types. Hence this feature is deprecated as of now even though still functional.**

Arrays can be transformed via HULL too. A transformation is triggered by providing a single element to the array which is a string transformation:

```yaml
some_object_key_with_an_array_of_strings_value:
- "_HULL_TRANSFORMATION_<<<NAME=TRANSFORMATION_NAME>>><<<ARGUMENT1=...>>><<<ARGUMENT2=...>>>"
```

Note that the result of the transformation needs to be an array with possible multiple entries depending on the executed transformation.

Transformation short forms are supported here same as for string properties, for example:

```yaml
some_object_key_with_an_array_of_strings_value:
- _HT!
    [ 
      {{ (index . "$").Values.hull.config.specific.some_referenced_value }}, 
      "another_value",
      "and_another_value"
    ]
```

### Example of a complex custom transformation

The HULL library comes with the predefined `hull.util.transformation.tpl` transformation which adds a crucial functionality to HULL rendered string and object values. While the principal HULL concept is to provide full control over all object values to the creators and consumers directly it might be required to still wrap logic decisions in the creation of some string, dictionary or string array values. A very typical example might be the arguments to a containers command which could depend on custom application specific fields the user should be able to define. It can be argued that this adds in a functionality that is the most basic in the regular helm workflow. In HULL this should be used with care but allows more flexibility for some HULL rendered objects that would otherwise be missing.

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
      custom_args:
        pod:
          containers:
            main:
              image:
                repository: my/image/repo
                tag: "99.9"
              args: _HT![
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
    app.kubernetes.io/component: custom_args
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.20.0
    helm.sh/chart: hull-test-1.20.1
  name: release-name-hull-test-custom_args
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: custom_args
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      labels:
        app.kubernetes.io/component: custom_args
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.20.0
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

## Provided transformations

The following basic transformations are provided by HULL. Extending this with custom helper transformations to allow to do specific operations in a concise manner is possible, for example:

- prefixing/suffixing referenced fields
- concatenation of referenced fields
- ...

The `tpl` transformation basically offers full flexibility and can be used for all allowed transformation scenarios but this comes at the price of more complex specification of the logical requirements.

### Get a value (_hull.util.transformation.get_)

#### __Arguments__ 

- REFERENCE: The referenced key within `values.yaml` to get the value from. The key path needs to be specified starting from `.Values` only, for exampe `hull.config.specific.value_to_get`.

#### __Produces__

The value of the referenced key within `values.yaml`. 

#### __Description__

Provides an easy to use shortcut to simply get the value of a field in `values.yaml`. This is supported for referenced values of simple types (string, integer or boolean). Getting array and dictionary values as they are is also supported as of now, however there can't be any further transformations embedded in the referenced structure. For more complex get operations use the `hull.util.transformation.tpl` transformation to format or process the result before returning it.

#### __Short Form Examples__

```yaml
string: _HT*hull.config.specific.string_value_to_get
```

### Create dynamic fullname (_hull.util.transformation.makefullname_)

#### __Arguments__

- COMPONENT: The static component name

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

- CONTENT: The string that might contain templating expressions

#### __Produces__

The processed result of executing `tpl` on the string. Depending on where this transformation is used this can be a dictionary, a string or an array of strings.

#### __Description__

The most powerful transformation that allows to freely specify the Go templating expression(s) to be evaluated. Care needs to be taken so that the returned string can be converted to the desired return type if it is not string.

#### __Short Form Examples__

```yaml
string: _HT!{{ printf "%s-%s" (index . "$").Values.hull.config.specific.
  prefix_value_to_get (index . "$").Values.hull.config.specific.
  suffix_value_to_get }}


array: # (⚠️ deprecated array transformation ⚠️)
- _HT!
    [ 
      {{ (index . "$").Values.hull.config.specific.prefix_value_to_get }}, 
      {{ (index . "$").Values.hull.config.specific.suffix_value_to_get }}
    ]

ports: # (⚠️ deprecated dictionary transformation ⚠️)
  _HT!:
    "_": |-
      {
         first: { containerPort: {{ (index . "$").Values.hull.config.specific.port_one }} },
         second: { containerPort: {{ (index . "$").Values.hull.config.specific.port_two }}  }
      }
```

### Evaluate a condition to a boolean with `tpl` (_hull.util.transformation.bool_)

#### __Arguments__

- CONDITION: The string that contains the literal condition to be checked against

#### __Produces__

A boolean return value that can be used to populate a boolean field. There is no need to supply outer `{{` and `}}` templating signs because the CONDITITION is already assumed to be within these curly braces to save typing.

#### __Description__

Typical use of this function is to set the `enabled` field on objects depending on a particular condition. Internally it uses `tpl` to produce a boolean result from the evaluation of the literal CONDITION.

The `enabled` fields explicitly allow string as an input which makes them subjectable to this transformation returning the boolean result.

#### __Short Form Examples__

```yaml
bool_field: _HT?and 
  (index . "$").Values.hull.config.specific.switch_one_enabled (index .
  "$").Values.hull.config.specific.switch_two_enabled
```

### Create a dictionary with `selector` labels for a given name (_hull.util.transformation.selector_)

#### __Arguments__

- COMPONENT: The string that contains the name of the component to create selector dictionary for

#### __Produces__

A dictionary return value that can be used to populate a `selector` field.

#### __Description__

Typical use of this function is to set the `matchLabels` field on a `networkpolicy`'s `podSelector`. By using this transformation the `matchLabels` will automatically be inline with the default HULL `selector` labels.

#### __Short Form Examples__

```yaml
podSelector:
  matchLabels: _HT&mycomponentname
```

---
Back to [README.md](./../README.md)