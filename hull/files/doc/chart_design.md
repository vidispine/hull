# Chart Design Guide

HULL offers multiple means to reduce the effort and repetition often associated with writing Helm charts. 
Within a single Helm charts you often want to define a particular value once and reference it in several places. There are multiple ways to achieve this and which one to select depends on the specific scenario. This page aims at giving an introduction on the methods that are at your disposal and helping you to choose the best one for each scenario.

## Referencing source values via transformations

When there are fields which need to be referenced in multiple places across different object instances of maybe even various object types, the best strategy is often to define the single source values in the `hull.config.specific` section and create references to these fields where they are required. References can be created by using the transformations as described [in the transformation documentation](./transformations.md). This is a frequent modeling scenario.

For example, assume we have a Helm chart with applications depending on the same database connection and one of the applications (call it `app-python`) requires the information as dedicated environment variables for `host`, `port`, `databaseName`, `username` and `password`. Another application `app-java` may want to be fed the same information as a database connection string.

To efficiently solve this you could create dedicated source fields:

```
hull:
  config:
    specific:
      database:
        host:
        port:
        name:
        username:
        password:
```

which are handed over as environment variables to `app-python`:

```
hull:
  objects:
    deployment:
      app-python:
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-python
                tag: 23.3.2
              env:
                DATABASE_HOST:
                  value: _HT*hull.config.specific.database.host
                DATABASE_PORT:
                  value: _HT*hull.config.specific.database.port
                DATABASE_NAME:
                  value: _HT*hull.config.specific.database.name
                DATABASE_USERNAME:
                  value: _HT*hull.config.specific.database.username
                DATABASE_PASSWORD:
                  value: _HT*hull.config.specific.database.password
```

and are combined to a database connection string for `app-java` maybe like this:

```
hull:
  objects:
    deployment:
      app-java:
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-java
                tag: 23.3.2
              env:
                DATABASE_CONNECTIONSTRING:
                  value: _HT!
                    {{ printf "%s%s:%s;databaseName=%s;user=%s;password=%s;" 
                      "jdbc:sqlserver://" 
                      (index . "$").Values.hull.config.specific.database.host
                      ((index . "$").Values.hull.config.specific.database.port | toString)                      
                      (index . "$").Values.hull.config.specific.database.name
                      (index . "$").Values.hull.config.specific.database.username
                      (index . "$").Values.hull.config.specific.database.password
                    }}

```

So for direct references without the need to change the source value it is feasible to use `_HT*` which also does automatic type conversions between standard types. However if some sort of data processing is required, `_HT!` is the tool to use due to the flexibility and power it provides, yet coming at the cost of a slightly more complicated usage. Again, please check [the transformation documentation](./transformations.md) for details.

## Object Type Defaulting methods

In other scenarios the formerly discussed method of using transformations to reference shared source values is not efficient enough to significantly reduce the data required for writing the chart. This is mostly when there is a large part of intended similarity between _all_ or _many_ instances of an object type. For this HULL offers mechanisms to default object instances from templates. 

First we will discuss the older `_HULL_OBJECT_TYPE_DEFAULT_` method and then the enhanced `sources` method for object instance defaulting.

### Using `_HULL_OBJECT_TYPE_DEFAULT_` to instantiate _all_ object instances with default values

For any object type which is covered by HULL it is possible to set properties to the specially named instance `_HULL_OBJECT_TYPE_DEFAULT_` and the values set here are copied to all other rendered instances of the same object type. After these default values are set the individual object instance properties are merged on top of the default values.

To e.g. set some helm hook annotations on all `configmap` instances you can simply do this:

```
hull:
  objects:
    configmap:
      _HULL_OBJECT_TYPE_DEFAULT_:
        annotations:
          helm.sh/hook: pre-install,pre-upgrade
          helm.sh/hook-delete-policy: before-hook-creation
          helm.sh/hook-weight: "-80"
      appconfig:
        data: 
          config: 
            inline: some configuration stuff


```

After rendering, the `appconfig` ConfigMap (and all other ConfigMaps that may be defined) will contain the helm hook annotations.

There is however more to this than just setting fixed values because you can also apply defaults to lower level properties of the same type. This example shows how you can add a liveness and a ready probe to all containers of all your `deployment`s:

```
hull:
  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_:
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              livenessProbe:
                httpGet:
                  path: /_health
                  port: http
                initialDelaySeconds: 60
                failureThreshold: 20
                successThreshold: 1
                periodSeconds: 30
                timeoutSeconds: 20
              readinessProbe:
                httpGet:
                  path: /_health
                  port: http
                initialDelaySeconds: 30
                successThreshold: 1
                failureThreshold: 4
                periodSeconds: 15
                timeoutSeconds: 20
```

For many sub elements in the object definitions - those which are treated explicitly as key-value dictionaries by HULL instead of the Kubernetes arrays as which they are rendered - it is allowed to also use the `_HULL_OBJECT_TYPE_DEFAULT_` special instance key word and the defined properties under this key will be merged into all subelements of this type. 

You can check the `values.yaml` for a extensive listing of where this is possible, in short you can use `_HULL_OBJECT_TYPE_DEFAULT_` for defaulting subelements for these properties:

- for `rules` fields in `role` and `clusterrole` definitions
- for `ports` fields in `service` definitions
- for `tls` and `rules` fields in `ingress` definitions. 

  Within the `rules` the `http.paths` are also defaultable this way
- for `initContainers`, `containers` and `volumes` fields in `pod` definitions. 

  Within `containers` and `initContainers` the `env`, `envFrom` and `volumeMounts` are also defaultable this way
- for `webhooks` fields in `mutatingwebhookconfiguration` and `validatingwebhookconfiguration` definitions

The described mechanism is in this regard different to the transformation method described above since it allows to apply default values to a large number of properties in an efficient manner. 

⚠️ Note that in terms of processing, HULL first applies transformations to all values in the `hull` dictionary before applying any `_HULL_OBJECT_TYPE_DEFAULT_` defaulting and copying of values. This sequence can be used to your advantage since you can use transformations in the `_HULL_OBJECT_TYPE_DEFAULT_` blocks which are processed first before the calculated values are written to all instances of the given object type. ⚠️

Returning to the database connection example, to set the database connection env vars to all containers of all deployments this is how you can combine both methods:

```
hull:
  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_:
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              env:
                DATABASE_HOST:
                  value: _HT*hull.config.specific.database.host
                DATABASE_PORT:
                  value: _HT*hull.config.specific.database.port
                DATABASE_NAME:
                  value: _HT*hull.config.specific.database.name
                DATABASE_USERNAME:
                  value: _HT*hull.config.specific.database.username
                DATABASE_PASSWORD:
                  value: _HT*hull.config.specific.database.password
                DATABASE_CONNECTIONSTRING:
                  value: _HT!
                    {{ printf "%s%s:%s;databaseName=%s;user=%s;password=%s;" 
                      "jdbc:sqlserver://" 
                      (index . "$").Values.hull.config.specific.database.host
                      ((index . "$").Values.hull.config.specific.database.port | toString)
                      (index . "$").Values.hull.config.specific.database.name
                      (index . "$").Values.hull.config.specific.database.username
                      (index . "$").Values.hull.config.specific.database.password
                    }}
                
      app-python:
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-python
                tag: 23.3.2
      app-java:
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-java
                tag: 23.3.2
```

To some degree using `required` properties in the JSON schema can interfere with the `_HULL_OBJECT_TYPE_DEFAULT_` mechanism. It may be required to specify some fields such as the `image` definition to satisfy the schemas required field restrictions since the schema is not aware of the `_HULL_OBJECT_TYPE_DEFAULT_` defaulting possibility and hence cannot know if a required property is set at a later stage after rendering. It is up to discussion if required schema definitions may be removed to allow more extensive usage of the `_HULL_OBJECT_TYPE_DEFAULT_` method. 

### Using `sources` field to combine _multiple_ default templates in a flexible manner

While the described methods of using HULL transformations and `_HULL_OBJECT_TYPE_DEFAULT_` defaulting (and the combination of both) are good means to reduce unnecessary repetetive code, there are still some frequent usecases which are not covered efficiently so far. 

Assume you have not one class of deployments where all instances are similar but maybe two or three classes where each class shares similar properties but the classes themselves are pretty much different from each other. Using `_HULL_OBJECT_TYPE_DEFAULT_` defaulting will not work great because it will always affect all object instances and there may be no suitable subset of properties which is sharable efficiently between the different classes. 

To support these use cases, HULL now offers the usage of the `sources` field which is a property of `hull.ObjectBase.v1` and can be applied to any object instance. `sources` is an array field and each entry must reference an instance key. By default the isntance key referenced must be of the same object type but you can even refernce instances from a different type as explained later. The source values of all `sources` entries are copied to the referencing object instance in the order they are defined.

Again using the database example, as you might have noticed the previous solution was not covering the different needs of `app-python` and `app-java` very good when obtaining the database connection data. In the `_HULL_OBJECT_TYPE_DEFAULT_` based example, all environment variables where shared by all pods which is actually not the intention. To improve upon that we define dedicated source objects and refer to them in the `sources` field. As you can see it is now efficient and precise to create even more deployments based on this setup:

```
hull:
  objects:
    deployment:
      single-database-fields:
        enabled: false
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              env:
                DATABASE_HOST:
                  value: _HT*hull.config.specific.database.host
                DATABASE_PORT:
                  value: _HT*hull.config.specific.database.port
                DATABASE_NAME:
                  value: _HT*hull.config.specific.database.name
                DATABASE_USERNAME:
                  value: _HT*hull.config.specific.database.username
                DATABASE_PASSWORD:
                  value: _HT*hull.config.specific.database.password
      database-connection-string:
        enabled: false
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              env:
                DATABASE_CONNECTIONSTRING:
                  value: _HT!
                    {{ printf "%s%s:%s;databaseName=%s;user=%s;password=%s;" 
                      "jdbc:sqlserver://" 
                      (index . "$").Values.hull.config.specific.database.host
                      ((index . "$").Values.hull.config.specific.database.port | toString)
                      (index . "$").Values.hull.config.specific.database.name
                      (index . "$").Values.hull.config.specific.database.username
                      (index . "$").Values.hull.config.specific.database.password
                    }}
      app-python-1:
        sources:
        - single-database-fields
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-python-1
                tag: 23.3.2
      app-python-2:
        sources:
        - single-database-fields
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-python-2
                tag: 23.3.2
      app-two-1:
        sources:
        - database-connection-string
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-two-1
                tag: 23.3.2
      app-two-2:
        sources:
        - database-connection-string
        pod:
          containers:
            main:
              image: 
                repository: myrepo/app-two-2
                tag: 23.3.2

```

An important things to note on how using `sources` works is that the introduction of `sources` should not break the `_HULL_OBJECT_TYPE_DEFAULT_` method of supplying defaults. To achieve this the following rules apply:
  - when no `sources` field is present, defaults are loaded from `_HULL_OBJECT_TYPE_DEFAULT_` if there are any defined. This way down-ward compatibility is preserved to existing charts.
  - when `sources` is present and empty, no defaults are loaded at all. This allows to opt out of applying `_HULL_OBJECT_TYPE_DEFAULT_` for particular object instances
  - when `sources` is present and only contains single entry `_HULL_OBJECT_TYPE_DEFAULT_`, the behavior is effectively the same as omiting the `sources` key altogether. Only the `_HULL_OBJECT_TYPE_DEFAULT_` defaults are loaded if any are provided.
  - otherwise any entries in the `sources` field are merged in the provided order (potentially including `_HULL_OBJECT_TYPE_DEFAULT_` if included in the list)

⚠️ Normally you would want to set `enabled: false` on the instances that serve as a basis for defaulting but technically this is not a strict requirement, they may also be rendered out with `enabled: true` if that is desired and the definitions are fledged out fully. 

However, setting `enabled: false` on any object instance will disable JSON schema validation for the specified object instance. Hence specifying only partial fragments for defaulting is feasible and the disabled instance as a whole does not need to pass any JSON schema validation making it suitable for use as individual building blocks. ⚠️

In some cases it may be desirable to share default data between objects of different types. Consider for example a scenario where pods should share an identical set of environment variables or volume mounts. To cater for this it is possible to reference an object instance from another (structure compatible!) object type by appending the `hull.object` type in brackets. To illustrate, this example sketches how defaults for a deployment may be loaded from a job instance:

```
hull:
  objects:
    job:
      load-this-from-deployment:
        enabled: false
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              env:
                LOADED_FROM_JOB:
                  value: external___loaded
    deployment:
      some-deployment:
        sources:
        - load-this-from-deployment[job]
        pod:
          containers:
            main:
              image: 
                repository: myrepo/myapp
                tag: 23.3.2
```

In the output you can find the LOADED_FROM_JOB environment variable being set in the deployments container.

### Using `sources` to share properties between pods and containers across workloads

An extension of the `sources` templating mechanism allows to define reusable and combinable templates for pods and containers. While the `sources` on the object instance type allow to share traits between instances of the same object type, the pod `sources` can be reused between all pod-based workloads `pod` specifications and the container `sources` can be reused between `containers` and `initContainers` across all pods. The logic of working with pod and container `sources` is the same as with the object instance `sources`.

#### Defining pod and container defaults

To have a set of properties added to pod or container specs, refer to the following structure where sets of properties may be defined:

```
hull:
  config:
    templates:
      pod:
        global: {}
      container:
        global: {}
```

For pods, any property you want to generally set on all pods you may put into the `global` dictionary. By default, these properties will be added to the pod specifications. For example, if you want to make sure that all your pods use the same `serviceAccountName` and run without root rights you could add the following to `global`:

```
hull:
  config:
    templates:
      pod:
        global: 
          serviceAccountName: my-service-account
          securityContext:
            runAsNonRoot: true
```

If you have other sets of properties you wish to reuse often, just define them under a self-chosen dictionary key. Assuming you have a fixed affinity (say to nodes with a particular graphic card) and you would like some of your pods to be placed on the corresponding nodes, you can specify this in the following manner:

```
hull:
  config:
    templates:
      pod:
        graphic-card-affinity: 
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: my.nodetype/graphic-card
                    operator: "In"
                    values:
                    - "true"
```

The same flexibility is provided for defaulting containers. In this `hull.config.templates` context, `container` refers to both `containers` and `initContainers` (not `ephemeralContainers`). 

To set globally applied properties on all containers again use the `global` dictionary. For example, to have an important environment vriable populated in all your containers use the `global` dictionary:

```
hull:
  config:
    templates:
      container: 
        global:
          env:
            'PROJECT':
              value: "The name of this project"
```

Same as with the pod `sources`, you may freely define more templates for shared properties to assign them to `containers` or `initContainers` at will.

#### Using pod and container defaults

Similar to the object instance `sources`, to load particular sources use the `sources` property on the pod and container specification level. When not specifying `sources` on a pod or container, the respective `global` defaults are being applied. When specifying a list of `sources`, the listed `sources` will be merged in the given order and lastly the pod or container specification is merged on top. Any defaulted data that is being added via the object instance `sources` or `_HULL_OBJECT_TYPE_DEFAULT_` is merged prior to the step where `pod` and `container` templates are applied. Please note that when you specify `sources` on pods or containers, the `global` source needs to be explicitly added in the list, otherwise it is not being applied. This is mainly to stay congruent with how the `sources` feature works with the object instances.

Here is a complex example combining pod and container `sources` usage. It sketches some fictional application that deals with graphic processing and has special requirements:

```
hull:
  config:
    templates:
      container: 
        global:
          env:
            'PROJECT':
              value: "The name of this project"
        high-resources:
          resources:
            limits:
              cpu: "5.5"
              memory: 9.9Gi
            requests:
              cpu: "5.5"
              memory: 9.9Gi
      pod:
        graphic-card-affinity: 
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: my.nodetype/graphic-card
                    operator: "In"
                    values:
                    - "true"
  objects:
    deployment:
      my-graphic-app:
        pod:
          sources: 
          - graphic-card-affinity
          ...
          initContainers:
            get-graphics-card:
              ...
            prepare-job:
              sources:
              - high-resources
              ...
          containers:
            renderer:
              sources:
              - global
              - high-resources
              ...
```
The following intentions are expressed in the example:

- for containers, generally an env var is to set on all containers by default

- a particular resource definition template is provided as `high-resources`

- for pod `templates` a `graphic-card-affinity` is defined for pushing pods to the corresponding nodes

- within the deployment `my-graphic-app` the following is configured:

  - add affinity via `graphic-card-affinity` pod source

  - the `get-graphics-card` initContainer does not have a `sources` field specified. Hence it will by default load the env var from the `container.global` source

  - the `prepare-job` initContainer explicitly refers to `source` `high-resources` and thus will be equipped with the correponding resource settings. Note that it excludes global in the sources list and hence will not have the env var set!

  - the `renderer` container does refer to `global` and `high-resources` `sources` and will therefore contain both the env var as well as the resource settings.

The dry-run rendered output delivers on the expectations:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: my-graphic-app
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-my-graphic-app
  namespace: default
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: my-graphic-app
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      labels:
        app.kubernetes.io/component: my-graphic-app
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.31.0
        helm.sh/chart: hull-test-1.31.0
      namespace: default
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: my.nodetype/graphic-card
                operator: In
                values:
                - "true"
      containers:
      - env:
        - name: PROJECT
          value: The name of this project
        image: renderer
        name: renderer
        resources:
          limits:
            cpu: "5.5"
            memory: 9.9Gi
          requests:
            cpu: "5.5"
            memory: 9.9Gi
      imagePullSecrets:
      - name: release-name-hull-test-example-registry
      - name: release-name-hull-test-local-registry
      initContainers:
      - env:
        - name: PROJECT
          value: The name of this project
        image: get-graphics-card
        name: get-graphics-card
      - image: prepare-job
        name: prepare-job
        resources:
          limits:
            cpu: "5.5"
            memory: 9.9Gi
          requests:
            cpu: "5.5"
            memory: 9.9Gi
      serviceAccountName: release-name-hull-test-default
```

This wraps up the introduction into efficient chart building with HULL.

---
Back to [README.md](./../../../README.md)