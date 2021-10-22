# Using and creating Transformations

Helm itself has by design no support for templating within the `values.yaml`. The `values.yaml` itself must be valid YAML and must not contain templating expressions. HULL can overcome this limitation to a certain degree.

As a simple example, it is often efficient to at least have possibilities to simply cross-reference fields in the `values.yaml`. One way this can be achieved is by using YAML anchors, the downside here is that an anchor and the reference to it need to be in the same YAML file. Considering that one main feature of Helm is to allow merging of multiple `values.yaml`'s this approach is very limited in scope.

The HULL library provides mechanism to work around this and provide this possibility. The mechanism for this is called transformations and is extensible for even way more complex tasks by allowing to inject complex Go Templating expressions in property values of the `values.yaml`. 

## Technical Background

Technically the objects defined in the `values.yaml` are preprocessed before they are converted to Kubernetes objects. In the first internal step, Helm merges all fields of all `values.yaml`'s involved into a single YAML structure. This YAML tree is then processed key-by-key by HULL and here it becomes possible to modify the YAML to the desired result by adding special keys and values to the YAML sections. When a transformation is detected during the `values.yaml` preprocessing by HULL an associated Go Templating function is called and the result replaces the transformation instruction in the YAML.

⚠️ It is important to consider the fact that when a dictionary is traversed in Go Templating it is done in an alphanumeric fashion. So in order to reference an itself transformed value succesfully it must be have a lower alphanumeric key in the dictionary hierarchy. However, since typically you would want to resolve a global value for configuration of your `hull.objects` properties in multiple places you should put your referenced value in the `hull.config.specific` section and then you can access it anytime when creating the objects. When you keep the alphanumeric processing order in mind it is furthermore no problem to use transformations on `hull.config.specific` properties too and later have the transformation result referenced by a transformation in the `hull.objects` section.⚠️

Some transformations are part of the HULL library and can be used out of the box. It is also possible to create your own Go Templating function/transformation and use them where possible.

## Limitations

Currently transformations are supported for limited scenarios. You can use transformations to modify:

- values which are dictionaries
- values which are of string type
- values which are array elements and are of string type

⚠️ **Triggering transformations is based on the detection of a starting prefix (__\_HULL_TRANSFORMATION\___) in key names (for dictionary values) or string values so it is not 100% guaranteed that a chart does not use this expression as a key or value but otherwise even though it is highly unlikely.** ⚠️

## Transformations

This section will highlight a simple transformation example and one showcasing the full possibilities of this approach.
### Example of a simple string transformation 

One simple and  useful transformations is likely cross-referencing the value of a dedicated YAML field in several places in the `values.yaml` itself. As mentioned the YAML anchor approach is limited in usability so this is how you can do it using the `hull.util.transformation.get` transformation. 

Assuming you have a local docker registry endpoint you want to use as the registry for several container images, you can achieve this like this:

```yaml
hull:
  config:
    specific:
      globalRegistry: local.registry:5000 # this is the value I want to 
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
                registry: "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.get>>><<<REFERENCE=hull.config.specific.globalRegistry>>>" # and here
                repository: internal_app2
                tag: "latest"
```

Now when preprocessing in HULL takes place, the string starting with the key word `_HULL_TRANSFORMATION_` is signaling that this value is being dynamically derived by calling the transformation function. The expression above is taken apart to call the function with named arguments.

The general syntax for string transformations is:

- `_HULL_TRANSFORMATION_`: 

  Prefix indicating that a transformation is defined. All string transformations must start with this prefix.
  
  Arguments to the transformation are wrapped in `<<<ARGUMENT-NAME=ARGUMENT-VALUE>>>`

- `<<<NAME=hull.util.transformation.get>>>`: 

  The name of the transformation (the Go Template Function) to call is the only mandatory argument which is the first argument in the call. 

- `<<<REFERENCE=hull.config.specific.globalRegistry>>>`

  This argument is specific to the transformation. Here it references the key from which we want to get the value from in dot-notation.

⚠️ **Note that the arguments themselves cannot contain the start-of and end-of argument signifiers `<<<` and `>>>`! These are important for string-splitting the arguments to the transformation.** ⚠️

Now we can take a look at the transformation itself.

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
{{ $key }}: {{ $current }}
{{- end -}}
```

In the code above the value of the dot-notated key is retrieved via iteration over the path's elements. It is mandatory for all transformations to return result data as a yaml block containing the passed in `$key` variable as key:

```yaml
{{ $key }}: "<RESULT OF TRANSFORMATION>"
```

In the source YAML the dictionary value of key `$key` is now replaced by the transformations result before rendering. Note that the type of the result field does not have to be a string but it must validate against the Kubernetes API objects JSON schema. In most scenarios the input and output types are identical so you would use a string transformation to produce a string as result.

The final rendered output has the transformations successfully applied:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations: {}
  labels:
    app.kubernetes.io/component: external_app
    app.kubernetes.io/instance: RELEASE-NAME
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
      app.kubernetes.io/instance: RELEASE-NAME
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations: {}
      labels:
        app.kubernetes.io/component: external_app
        app.kubernetes.io/instance: RELEASE-NAME
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
        image: local.registry:5000/internal_app1:latest
        name: internal_one
        ports: []
        volumeMounts: []
      - env: []
        envFrom: []
        image: local.registry:5000/internal_app2:latest
        name: internal_two
        ports: []
        volumeMounts: []
```

### Example of a dictionary transformation

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

### Example of an array transformation

Arrays can be transformed via HULL too. A transformation is triggered by providing a single element to the array which is a string transformation:

```yaml
some_object_key_with_an_array_of_strings_value:
- "_HULL_TRANSFORMATION_<<<NAME=TRANSFORMATION_NAME>>><<<ARGUMENT1=...>>><<<ARGUMENT2=...>>>"
  ...
```

Note that the result of the transformation is an array with possible multiple entries depending on the executed transformation.

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
              args: 
              - "_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.tpl>>><<<CONTENT=
[
{{ if (index . \"PARENT\").Values.hull.config.specific.if_this_arg_is_defined }}
\"{{ (index . \"PARENT\").Values.hull.config.specific.if_this_arg_is_defined }}\",
\"{{ (index . \"PARENT\").Values.hull.config.specific.then_add_this_arg }}\",
{{ end }}
{{ if not (index . \"PARENT\").Values.hull.config.specific.if_this_arg_is_not_defined }}
\"{{ (index . \"PARENT\").Values.hull.config.specific.then_use_this_arg }}\"
{{ end }}
]
>>>"
```

The intention of the above configuration is to demonstrate some conditional population of the `args` array. It should result in three elements:

```yaml
- --this-is-defined # always as value of specific key if_this_arg_is_defined
- --hence-is-this # value of key then_add_this_arg should be added when key this-is-defined has a value
- --and-this-because-other-is-not-defined # value of key then_use_this_arg should be added when key if_this_arg_is_not_defined is not defined
```
On rendering the following happens:

- for `args` the transformation `hull.util.transformation.tpl` is executed on the string array. 
- the `CONTENT` argument is subjected to the `tpl` Go Templating function. This renders string input with potential placeholders. The `"`s need to be escaped with `\"` in the string. 

  Following additional rules apply to the usage of templating expressions in this manner:

  - when referring to the `.Values` in `values.yaml` you need to refer to 

    ```yaml
    (index . \"PARENT\").Values
    ```

    instead. This is because the parent charts context is being passed into the `tpl` function as a dictionary parameter `PARENT`. Nevertheless full access to all fields of the `values.yaml` is possible.

  - When the `tpl`-ed string should result in a string array, use the 

    ```yaml
    [\"value1\",\"value2\"] 
    ```

    notation to produce the resulting string array. This overcomes typical indentation pitfalls with the 

    ```yaml
    - value1
    - value2
    ```
    notation.

The rendered result again contains the intended `args` section:

```yaml
# Source: hull-test/templates/hull.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: custom_args
    app.kubernetes.io/instance: RELEASE-NAME
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
      app.kubernetes.io/instance: RELEASE-NAME
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      labels:
        app.kubernetes.io/component: custom_args
        app.kubernetes.io/instance: RELEASE-NAME
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

The `tpl` transformation basically offers full flexibility and can be used for all allowed transformation scenarios but this comes at the price of complex specification requirement.
### Get a value (_hull.util.transformation.get_)

Arguments: 

- REFERENCE: The referenced key within `values.yaml` to get the value from

Produces: 

The value of the referenced key within `values.yaml`

### Create dynamic fullname (_hull.util.transformation.makefullname_)

Arguments: 

- COMPONENT: The static component name

Produces:

The processed fullname, typically `<CHART_NAME>_<RELEASE_NAME>_<COMPONENT>`

### Render a string with `tpl` (_hull.util.transformation.tpl_)

Arguments: 

- CONTENT: The string that might contain templating expressions

Produces:

The processed result of executing `tpl` on the string. Depending on where this transformation is used this can be a dictionary, a string or an array of strings.

---
Back to [README.md](./../README.md)