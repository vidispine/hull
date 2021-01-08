# Using and creating Transformations

Helm itself has by desgin no support for templating within the `values.yaml`. The `values.yaml` must be valid YAML and must not contain templating expressions. 

However it is often efficient to at least have possibilities to simply cross-reference fields in the `values.yaml`. One way this can be achieved is by using YAML anchors, the downside here is that an anchor and the reference to it need to be in the same YAML file. Considering that one main feature of Helm is to allow merging of multiple `values.yaml`'s this approach is very limiting in scope.

The HULL library provides mechanism to work around this. It is called transformations and is extensible for other tasks. 

## Technical Background

Technically the objects defined in the `values.yaml` are preprocessed before they are converted to Kubernetes objects. By adding special keys and values to the YAML sections it becomes possible to modify the YAML to the desired result. When a transformation is detected during the `values.yaml` preprocessing an associated Go Templating function is called and the result added to the YAML.

Some transformations are part of the HULL library and can be used out of the box. It is also possible to create your own Go Templating function/transformation and use them where possible.

## Limitations

Currently transformations are only supported for transforming string and dictionary values. It is based on the detection of a key word (__HULL_TRANSFORMATION__) in key names or string values so it is not 100% guaranteed that a chart does not use this expression otherwise even though it is unlikely.

So there is no guarantee that this works in all scenarios but it can be a really useful addition to enhance your charts functionality.

## Transformations

Check the first transformation for a deeper explanation of how transformations work.

### Example of a string transformation 

One of the most useful transformations is likely referencing the value of a dedicated YAML field in several places in the `values.yaml`. 

Assuming you have a local docker registry endpoint you want to use as the registry for several container images, you can achieve this like this:

```yaml
hull:
  config:
    specific:
      globalRegistry: local.registry:5000 # this is the value I want to reuse

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
                registry: "_HULL_TRANSFORMATION_{{NAME=hull.util.transformation.get}}{{REFERENCE=hull.config.specific.globalRegistry}}" # here it is used
                repository: internal_app1
                tag: "latest"

            internal_two:
              image: 
                registry: "_HULL_TRANSFORMATION_{{NAME=hull.util.transformation.get}}{{REFERENCE=hull.config.specific.globalRegistry}}" # and here
                repository: internal_app2
                tag: "latest"
```

Now when preprocessing takes place, the string starting with the key word `_HULL_TRANSFORMATION_` is signaling that this value is being dynamically derived by calling the transformation function. The expression above is taken apart to call the function with named arguments.

The general syntax used is:

- `_HULL_TRANSFORMATION_`: 

  Indicates a transformation. 
  
  Arguments to the transformation are wrapped in `{{<ARGUMENT-NAME>=<ARGUMENT-VALUE>}}`

- `{{NAME=hull.util.transformation.get}}`: 

  The name of the Go Template Function to call is the only mandatory argument which is the first argument in the call.

- `{{REFERENCE=hull.config.specific.globalRegistry}}`

  This argument is specific to the transformation. Here it references the key from which we want to get the value from in dot-notation.

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

In the code above the value of the dot-notated key is retrieved via iteration over the path's elements. It is mandatory for transformations to return result data as a yaml block containing the `$key` variable as key:

```yaml
{{ $key }}: "<RESULT OF TRANSFORMATION>"
```

In the source YAML the value of `$key` is now replaced by the transformations result. Note that the type of the result field does not have to be a string but it must validate against the Kubernetes API objects JSON schema. In most scenarios the input and output types are identical so you would use a string transformation to produce a string as result.

The rendered output has the transformations successfully applied:

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

Input type validation might demand an `object` as an input fields type. Similar to the string transformation presented above you can then also trigger a transformation by a dictionary as input. In this case provide the following dictionary value to the key you wish to process:

```yaml
_HULL_TRANSFORMATION_:
  NAME: 
  ARGUMENT1:
  ARGUMENT2:
  ...
```
## Provided transformations

The following basic transformations are provided by HULL. Extending this with custom transformations to do more elaborate operations is possible, for example:

- prefixing/suffixing referenced fields
- concatenation of referenced fields
- ...

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
