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

⚠️ **Triggering transformations is based on the detection of a starting prefix __\_HULL_TRANSFORMATION\___ or __\_HT__ for built-in transformation short forms in key names (for dictionary values) or string values so it is not 100% guaranteed that a chart does not use this expression as a key or start of a value but otherwise it is highly unlikely.** ⚠️

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
                registry: _HT*hull.config.specific.globalRegistry # and here, just a briefer syntax for the same transformation
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

As HULL comes with a predefined set of handy transformations and always typing down the regular transformation interface structure described above is pretty inconvenient, there exist so-called __short forms__ to these built-in transformations. The short forms take advantage of the fact that all built-in transformations only demand a single argument so these transformation call can be done with much less typing.

⚠️ **Short forms are the prefered way to trigger transformations since functionally they are fully equivalent to the long form versions but are much easier to read and write** ⚠️

In the above example we used the short form for the `hull.util.transformation.get` transformation like this: 

```yaml
registry: _HT*hull.config.specific.globalRegistry # and here
```

which is equivalent to writing:

```yaml
registry: "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.get>>><<<REFERENCE=hull.config.specific.globalRegistry>>>"
```

but much shorter. The full transformation call is reduced to a short prefix (`_HT`), a character indicating the specific transformation to use (`*` for `hull.util.transformation.get`) and the single arguments (`REFERENCE`) value without the need to specify the arguments name. The other possible characters for short forms are `?`, `!`, `/`, `^` and `&` and  the following transformation short forms are available for use:

- `_HT*`: `hull.util.transformation.get`
- `_HT?`: `hull.util.transformation.bool`
- `_HT!`: `hull.util.transformation.tpl`
- `_HT/`: `hull.util.transformation.include`
- `_HT^`: `hull.util.transformation.makefullname`
- `_HT&`: `hull.util.transformation.selector`

Besides this set of basic transformation short forms, some special short form combinations exist which further help in writing compact configuration code:

- `_HT?/`: `hull.util.transformation.bool` + `hull.util.transformation.include`
- `_HT!*`: `hull.util.transformation.tpl` + `hull.util.transformation.get`

The functionality and usage of the short form combinations is explained after all single short forms have been described in detail which is subject of the next chapter. 


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
|   SOURCE_PATH: The path elements leading up to this field
|   RETURN_TEMPLATE_STRING: If true, returns a templating expression which can be 
|                           used with tpl to resolve this fields value. If false, 
|                           the resolved value itself is returned.
|
*/ -}}
{{- define "hull.util.transformation.get" -}}
{{- $parent := (index . "PARENT_CONTEXT") -}}
{{- $key := (index . "KEY") -}}
{{- $reference := (index . "REFERENCE") -}}
{{- $sourcePath := default list (index . "SOURCE_PATH") -}}
{{- $returnTemplateString := default false (index . "RETURN_TEMPLATE_STRING") -}}
{{- $objectType := "" -}}
{{- $objectInstanceKey := "" -}}
{{- if (gt (len $sourcePath) 3) -}}
{{  if (eq (index $sourcePath 1) "objects") -}}
{{- $objectType = index $sourcePath 2 -}}
{{- $objectInstanceKey = index $sourcePath 3 -}}
{{- end -}}
{{- end -}}
{{- $templateString := "(index . \"$\").Values"  }}
{{- $current := $parent.Values -}}
{{- if hasPrefix "*" $reference -}}
{{- $reference = $reference | trimPrefix "*" -}}
{{- $current = toYaml $parent | fromYaml -}}
{{- $templateString = "(index . \"$\")"  }}
{{- end -}}
{{- $serializer := "" }}
{{- $getValue := include "hull.util.transformation.serialize.get" (dict "VALUE" $reference) | fromYaml -}}
{{- if $getValue.serialize -}}
{{- $reference = $getValue.remainder -}}
{{- if hasPrefix "*" $reference -}}
{{- $reference = $reference | trimPrefix "*" -}}
{{- $current = toYaml $parent | fromYaml -}}
{{- $templateString = "(index . \"$\")" }}
{{- end -}}
{{- $serializer = $getValue.serializer -}}
{{- end -}}
{{- $path := splitList "." $reference -}}
{{- $skipBroken := false}}
{{- $brokenPart := "" }}
{{- $details := "" -}}
{{- $isChartSpecialCase := false -}}
{{- if (eq (first $path) "Chart")  -}}
{{- $isChartSpecialCase = true -}}
{{- end -}}
{{- range $pathIndex, $pathElement := $path -}}
{{- if (and ($isChartSpecialCase) (eq $pathIndex 1)) -}}
{{- $pathElement = $pathElement | untitle -}}
{{- end -}}
{{- if eq $pathElement "§OBJECT_TYPE§" -}}
  {{- if ne $objectType "" -}}
    {{- $pathElement = $objectType -}}
  {{- else -}}
    {{- $skipBroken = true -}}
    {{- $brokenPart = $pathElement -}}
    {{- $details = printf "OBJECT_TYPE not set in current calling context, cannot get path %s" $reference }}
  {{- end -}}
{{- else -}}
  {{- if eq $pathElement "§OBJECT_INSTANCE_KEY§" -}}
    {{- if ne $objectInstanceKey "" -}}
      {{- $pathElement = $objectInstanceKey -}}
    {{- else -}}
      {{- $skipBroken = true -}}
      {{- $brokenPart = $pathElement -}}
      {{- $details = printf "OBJECT_INSTANCE_KEY not set in current calling context, cannot get path %s" $reference }}
    {{- end -}}
  {{- else -}}
    {{- $pathElement = regexReplaceAll "§" $pathElement "." }}
  {{- end -}}
{{- end -}}
{{- if (not $skipBroken) -}}
{{- if (regexMatch "^\\d+$" $pathElement) -}}
{{- $current = (index $current (int $pathElement)) -}}
{{- $templateString = printf "(index %s %s)" $templateString $pathElement }}
{{- else -}}
{{- if (or (hasKey $current $pathElement)) -}}
{{- $current = (index $current $pathElement) }}
{{- $templateString = printf "(index %s \"%s\")" $templateString $pathElement }}
{{- else -}}
{{- $skipBroken = true -}}
{{- $brokenPart = $pathElement -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
{{- if $skipBroken -}}
{{- if eq $details "" -}}
{{- $details = printf "Element %s in path %s was not found" $brokenPart $reference -}}
{{- end -}}
{{- if $returnTemplateString -}}
{{- include "hull.util.error.message" (dict "ERROR_TYPE" "HULL-GET-TRANSFORMATION-REFERENCE-INVALID" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- if $parent.Values.hull.config.general.debug.renderBrokenHullGetTransformationReferences -}}
{{ $key }}: BROKEN-HULL-GET-TRANSFORMATION-REFERENCE:Element {{ $brokenPart }} in path {{ $reference }} was not found
{{- else }}
{{- if $parent.Values.hull.config.general.errorChecks.hullGetTransformationReferenceValid -}}
{{- $key }}: {{ include "hull.util.error.message" (dict "ERROR_TYPE" "HULL-GET-TRANSFORMATION-REFERENCE-INVALID" "ERROR_MESSAGE" $details) -}}
{{- else -}}
{{- $key }}: ""
{{- end -}}
{{- end -}}
{{- end -}}
{{- else -}}
{{- if and (typeIs "string" $current) (not $current) }}
{{ $key }}: ""
{{- else -}}
{{- $convert := (include "hull.util.transformation.convert" (dict "SOURCE" $current "SERIALIZER" $serializer)) }}
{{- if (ne $serializer "") -}}
{{- $templateString = printf "(include \"hull.util.transformation.convert\" (dict \"SOURCE\" %s \"SERIALIZER\" \"%s\"))" $templateString $serializer }}
{{- end -}}
{{- if $returnTemplateString -}}
{{- $templateString -}}
{{- else -}}
{{ $key }}: {{ $convert }}
{{- end -}}
{{- end -}}
{{- end -}}
{{- end -}}
```

Without going too much into detail, in the code above the value of the dot-notated key is retrieved via iteration over the path's elements. Then it is either returned as an empty string (if non existent) or further processed with the `hull.util.transformation.convert` function which creates the return value based on `$current` type. It is capable of returning simple types (string, bool and integer values) but also complex types including nested dictionaries and arrays. In case of of a missing element in the given path it returns an error in form of a string which will be processed and converted to a speaking execution error of Helm in the end. A special use case is to set RETURN_TEMPLATE_STRING to true which will return a templating expression that resolves the fields value instead of the actual value of the field (required for `_HT!*` combined transformations).

It is mandatory for all transformations to return result data as a yaml block containing the passed in `$key` variable as key:

```yaml
{{ $key }}: "<RESULT OF TRANSFORMATION>"
```

In the source YAML the dictionary value of key `$key` is now replaced by the transformations result before rendering. Note that the type of the result field does not have to be a string but it must validate against the Kubernetes API objects JSON schema when deploying to Kubernetes. 

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
    app.kubernetes.io/version: 1.29.0
    helm.sh/chart: hull-test-1.29.0
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
        app.kubernetes.io/version: 1.29.0
        helm.sh/chart: hull-test-1.29.0
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

### Specifying transformations in form of a dictionary

A dictionary-form transformation is a transformation that is supposed to create a dictionary as the result and the transformation specification itself is also defined as a dictionary. This was the original way to process dictionaries with HULL transformations to comply with the need of the fields value to be a dictionary.

⚠️⚠️⚠️ **By now, HULL has full support to supply a string transformation instead of a boolean, integer, array or dictionary input value in `values.yaml` properties - even if the original Kubernetes schema demands the input value to be boolean, integer, array or object respectively. 'It is solely the responsibility of the configurator to make sure that any transformation returns an object of the correct input type and structure otherwise Kubernetes will not accept invalid objects upon deployment time. Technically the ability to use HULL string transformations everywhere is achieved by extension of the Kubernetes JSON schema to always allow a regex conforming 'transformation' string input besides the original type of the value. Currently the regex of allowed string input is `^\s*(_HT[\*|\?|\^|!|&|/]|_HULL_TRANSFORMATION_<<<).*`. By having this ability the dictionary and array form of the HULL transformations become mostly deprecated to generate complete lists or dictionaries.** ⚠️⚠️⚠️

Input type validation might demand an `object` as a values object type. Similar to the string transformation presented above you can then also trigger a transformation by providing a dictionary as input. In this case provide the following dictionary value to the key you wish to process:

```yaml
some_object_key_with_a_dictionary_value: 
  _HULL_TRANSFORMATION_:
    NAME: "TRANSFORMATION_NAME"
    ARGUMENT1: "..."
    ARGUMENT2: "..."
    ...
```

The presence of the `_HULL_TRANSFORMATION_` key as the value of the input object triggers the transformation. Instead of string-splitting arguments they are derived by the keys in the `_HULL_TRANSFORMATION_` dictionary.

If you use an available short form for a transformation you specify `_HT` plus the single transformation specific character (`*`, `?`, `!`,`^` or `&`) as the key. A single key is expected in the dictionary whose name can be chosen freely (suggestion is `_`) and the actual argument value for that keys value is the argument. For example, the structure presented above would look like this for the short form of the `hull.util.transformation.tpl` transformation:

```yaml
some_object_key_with_a_dictionary_value: 
  _HT!:
    "_": <CONTENT of the tpl transformation>
```

As mentioned, dictionary transformations are not required anymore to transform full dictionaries. The same can be achieved with less typing by putting in a `_HT` string-based definition of the transformation. However, the dictionary form still does have a very potent usability for combining existing dictionary entries with dynamically generated ones. This is best demonstrated by an example.

Assume you have a container in a pod-based object defined in your helm chart and this container is supposed to always have some standard `volumeMounts`, for example a configmap for application configuration. However, for certificate handling it may be required to mount a dynamic number of certificate files into the pod. A `volumeMounts` section which both has defined static entries and dynamic entries could look like this:

```yaml
volumeMounts:
  configmap: # a static volumeMount, always present unless set to enabled: false
    name: configmap
    mountPath: 'app/config/appsettings.json'
    subPath: appsettings.json
    hashsumAnnotation: true
  _HULL_TRANSFORMATION_: # a transformation trigger
    NAME: hull.util.transformation.tpl # do a tpl transformation
    CONTENT: |- # iterate over a dictionary with certificate file names and contents and add one volumeMount per provided file from a volume named certs which is supposed to contain the referenced certificate files
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


### Specifying transformations in form of an array

**It is not required anymore to use an array-form transformation to process an array in HULL with a transformation. By now HULL string transformations are available for objects of all input types.**

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

As highlighted more closely in the next chapter on string-based short form transformations, the same as above can be achieved with this syntax:

```yaml
some_object_key_with_an_array_of_strings_value: |- 
  _HT!
    [ 
      {{ (index . "$").Values.hull.config.specific.some_referenced_value }}, 
      "another_value",
      "and_another_value"
    ]
```


Due to the fact, that in the world of Helm it is not possible to merge arrays, there is no way to use this array transformation in the same way as the dictionary transformation to append entries to an array. Arrays (or lists) can only be overwritten entirely which is the reason why HULL has a strong focus on using dictionaries instead of Kubernetes native arrays in the places where this is possible.

### Example of a complex custom transformation

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
    app.kubernetes.io/version: 1.29.0
    helm.sh/chart: hull-test-1.29.0
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
        app.kubernetes.io/version: 1.29.0
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

More detailed on this feature is available in the below section on _hull.util.transformation.tpl_ transformations.

## Provided transformations

The following basic transformations are provided by HULL. Extending this with custom helper transformations to allow to do specific operations in a concise manner is possible, for example:

- prefixing/suffixing referenced fields
- concatenation of referenced fields
- ...

but this can be achieved with less effort by writing a reguler Helm `function` and call it with the `include` `_HT/` transformation. In this sense the `_HT/` opens the door to integrating additional reusable Helm `functions` while `_HT!` is the swiss-army knife to perform special operations in place. The `tpl` transformation basically offers full flexibility and can be used for all allowed transformation scenarios but this comes at the price of more complex specification of the logical requirements.

### Get a value (_hull.util.transformation.get_)

#### __Arguments__ 

- REFERENCE: 

  The referenced key within `values.yaml` to get the value from. The key path needs to be specified starting from `.Values` only, for exampe `hull.config.specific.value_to_get`. 

  Note that if any path element itself contains a dot (`.`) you can escape it with the `§` character to still be able to reference it, for example if you want to reference the key path:

  ```yaml
  hull:
    config:
        specific:
          'key.with.dots.in.it': hello dots!
  ```

  you can do so by using the HULL get transformation like this:

  `_HT*hull.config.specific.key§with§dots§in§it`

  Addionally, if used in a field beneath `hull.objects.<object_type>.<object_instance_key>`, it also possible to reference the current contexts `OBJECT_TYPE` and `OBJECT_INSTANCE_KEY` via special static keys: 
  
  - `§OBJECT_TYPE§` and 
  - `§OBJECT_INSTANCE_KEY§` 
  
  in the dotted path. The keys must be exactly written like this and if such a key is found, the replacing of `§` for `.` is of course not performed for this value. 
  
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

When used in the `values.yaml` context, any complex object (dictionary or array) referenced will in fact be inserted as an object with further leaves into the `values.yaml` tree. This is very powerful since it allows to reuse larger configuration parts multiple times. But in some cases you may want to serialize the referenced dictionary or list object into a JSON or YAML string, for this you have the additional possibility to prefix the REFERENCE with one of the following prefixes:

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

Consider using the `_HT*` reference style to address fields in the `values.yaml` for more compact style and less typing. The full range of `_HT*` usage is available, hence you can also use `_HT**` for root context access or serialization instructions as in `_HT*toJson|hull.config.xyz`.

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

### Call an `incude` function (_hull.util.transformation.include_)

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
    app.kubernetes.io/version: 1.29.0
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
      app.kubernetes.io/version: 1.29.0
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

---
Back to [README.md](./../README.md)