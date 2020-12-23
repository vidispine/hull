# HULL: Helm UtiLity Library

This Helm library chart is designed to ease building, maintaining and configuring Helm charts. When integrated as a sub chart into your Helm chart, specifying your deployments can be done by defining the wanted resources in the `values.yaml` file(s) under the `hull` subchart key. No template files in the `/templates` folder need to be created, adapted and maintained to define regular K8s objects when using the HULL library. 

When objects are defined in the `values.yaml` all Kubernetes YAML is rendered via the HULL library and the Go templating functions therein. JSON schema validation with the `values.schema.json` aids producing K8S conforming objects for deployment.

The HULL chart is inspired by the 'common' Helm chart concept:

https://github.com/helm/charts/tree/master/incubator/common

and uses [![Gauge Badge](https://gauge.org/Gauge_Badge.svg)](https://gauge.org) for testing.

## Feature Overview

As highlighted above, when included in a Helm chart the HULL library chart can take over the job of dynamically rendering K8S objects from their given specifications from the `values.yaml` file alone. With YAML object construction deferred to the HULL library functions instead of custom YAML templates in the `/templates` folder you can centrally enforce best practices:

- Concentrate on what is needed to specify objects without having to write boilerplate YAML templates. The single interface of the HULL library can be used to both create and configure objects in charts for deployment. To avoid misconfigurations, the library interface is JSON validated on input (e.g. when using VSCode) and rendering using the Helm integrated JSON Schema validation. Furthermore extensive unit tests create K8S objects which are validated against the Kubernetes API JSON schema.
- All objects by default get a unique Kubernetes `metadata.name` assigned based on the chart name, the release name and the objects component name.
- Uniform and rich metadata is automatically attached to all objects created by the HULL library. 
  - Kubernetes standard labels as defined in https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/ are added to all objects metadata automatically. 
  - Within a Helm chart including HULL, further custom metadata can be set for 
    - all created K8S objects or 
    - all objects of a given K8S type or 
    - individual K8S objects. 
- For all supported Kubernetes object types, all available Kubernetes properties are made available for configuration in Helm charts including the HULL library. Only updating the HULL chart to a newer Kubernetes API version is required to enable configuring new properties. The HULL charts are versioned to reflect the minimal Kubernetes API versions supported. 
- Enable automatic hashing of referenced configmaps and secrets to facilitate pod restarts on changes of configuration
- Flexible handling of ConfigMap and Secret input by choosing between inline specification of contents in `values.yaml` or import from external files for contents of larger sizes. When importing data from files the data can be either run through the templating engine or imported untemplated 'as is' if it already contains templating expressions that shall be passed on to the consuming application.

To learn more about the architecture of this library and it's features see ...

_IMPORTANT_: 

While there may be several benefits to rendering YAML via the HULL library please take note that it is a non-breaking addition to your Helm charts. The regular Helm workflow involving rendering of YAML templates in the `/templates` folder is completely unaffected by integration of the HULL library chart. Sometimes you might have very specific requirements on your configuration or object specification which the HULL library does not meet so you can use the regular Helm worflow for them and the HULL library for your more standard needs - easily in parallel in the same Helm chart. 

## Introduction

Take the nginx deployment example from the Kubernetes documentation https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment as a basis:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

To render this using the HULL library the following needs to be done:

- Create an "nginx" helm chart that should contain the nginx deployment. The templates folder can remain empty for now.
- Inlude the HULL library chart as a subchart
- Copy the `hull_init.yaml` from the HULL charts root folder to the `/templates` folder of your parent chart. This is the only manual step that needs to be taken in order to use the HULL library chart.

Now to render the nginx deployment example with minimal effort you need to create the following `values.yaml` file in your parent chart:

```yaml
hull:  
  objects:
    deployment:
      nginx: # specify the nginx deployment under key 'nginx'
        pod:
          replicas: 3
          containers:
            nginx:
              repository: nginx
              tag: 1.14.2
```

This produces the following rendered objects:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: nginx
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: "1"
    helm.sh/chart: hull-test-1
  name: release-name-hull-test-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/component: nginx
      app.kubernetes.io/instance: RELEASE-NAME
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      labels:
        app.kubernetes.io/component: nginx
        app.kubernetes.io/instance: RELEASE-NAME
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: "1"
        helm.sh/chart: hull-test-1
    spec:
      containers:
      - env: []
        envFrom: []
        image: nginx:1.14.2
        name: nginx
        ports: []
        volumeMounts: []
      initContainers: []
      serviceAccountName: release-name-hull-test-default
      volumes: []
---
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    general_custom_annotation_1: General Custom Annotation 1
    general_custom_annotation_2: General Custom Annotation 2
    general_custom_annotation_3: General Custom Annotation 3
  labels:
    app.kubernetes.io/component: default
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: "1"
    general_custom_label_1: General Custom Label 1
    general_custom_label_2: General Custom Label 2
    general_custom_label_3: General Custom Label 3
    helm.sh/chart: hull-test-1
  name: release-name-hull-test-default
```

This is a deployment with standard metadata auto-created and a service account associated with the deployment.

The following highlights some additional features that come with using the HULL library.

We can add custom metadata besides the standard metadata auto-created. The custom metadata labels and annotations can be applied to either all objects within this helm chart, all objects of a given type or just individual objects. 

The following `values.yaml` showcases all possibilities to set metadata:

```yaml
hull:
  config:
    general:       
      metadata:
        labels:         
          custom: # Add some custom labels to all objects created in this chart
            general_custom_label_1: General Custom Label 1
            general_custom_label_2: General Custom Label 2
            general_custom_label_3: General Custom Label 3
        annotations: 
          custom: # Add some custom annotations to all objects created in this chart
            general_custom_annotation_1: General Custom Annotation 1
            general_custom_annotation_2: General Custom Annotation 2
            general_custom_annotation_3: General Custom Annotation 3    
  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_: # this object key is used to set defaults per object type
        annotations:
          default_annotation_1:  Default Annotation 1
          default_annotation_2:  Default Annotation 2
          general_custom_annotation_3: Default Annotation 3 # overwrite the global default
        labels:
          default_label_1:  Default Label 1
          default_label_2:  Default Label 2
          general_custom_label_3: Default Label 3 # overwrites the global default
      nginx: # specify the nginx deployment under key 'nginx'
        pod:
          replicas: 3
          containers:
            nginx:
              repository: nginx
              tag: 1.14.2
```

The outcome will be a K8S deployment object being deployed to the cluster that looks like this (the ServiceAccount is left out):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    default_annotation_1: Default Annotation 1
    default_annotation_2: Default Annotation 2
    general_custom_annotation_1: General Custom Annotation 1
    general_custom_annotation_2: General Custom Annotation 2
    general_custom_annotation_3: Default Annotation 3
  labels:
    app.kubernetes.io/component: nginx
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: "1"
    default_label_1: Default Label 1
    default_label_2: Default Label 2
    general_custom_label_1: General Custom Label 1
    general_custom_label_2: General Custom Label 2
    general_custom_label_3: Default Label 3
    helm.sh/chart: hull-test-1
  name: release-name-hull-test-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/component: nginx
      app.kubernetes.io/instance: RELEASE-NAME
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations:
        default_annotation_1: Default Annotation 1
        default_annotation_2: Default Annotation 2
        general_custom_annotation_1: General Custom Annotation 1
        general_custom_annotation_2: General Custom Annotation 2
        general_custom_annotation_3: Default Annotation 3
      labels:
        app.kubernetes.io/component: nginx
        app.kubernetes.io/instance: RELEASE-NAME
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: "1"
        default_label_1: Default Label 1
        default_label_2: Default Label 2
        general_custom_label_1: General Custom Label 1
        general_custom_label_2: General Custom Label 2
        general_custom_label_3: Default Label 3
        helm.sh/chart: hull-test-1
    spec:
      containers:
      - env: []
        envFrom: []
        image: nginx:1.14.2
        name: nginx
        ports: []
        volumeMounts: []
      initContainers: []
      serviceAccountName: release-name-hull-test-default
      volumes: []
```



## Introduction & Motivation

In the context of Kubernetes and Helm there are basically two groups of people that work with Helm charts:
- the chart maintainers
- the chart users

### The chart maintainers view

When starting to work on Helm charts it very soon became apparent that some standard scenarios are not supported very well by Helm. Whilst there is much freedom given to the chart designers and maintainers in how to abstract the configuration, Helm offers no easy standard way to handle standard demands. 

Helm chart maintainers typically create and maintain a varying number of helm charts. Let's first take a look at aspects of helm chart creation from a creators point of view. Getting started on building helm charts is challenging, especially for someone not experienced with the concepts of Kubernetes, Helm, YAML and Go Templating and all the relations between them which are needed to create sound helm charts. Furthermore, YAML and string templating don't go well together which is something rightfully critized, it can become very finicky to produce valid YAML output with templating expressions. Typically starting a new helm chart from scratch requires a significant amount of copying and pasting templates from existing charts and adapting them to the new products needs. This is a time consuming and error prone process. 
 
Once charts have been created and published they need to be mainained. Maintaining a single halm chart can be reasonable done manually but let us assume it is required to maintain many helm charts, then the amount of (for the most part) duplicated YAML blocks in templates grows very fast. Assuming you need to fix a conceptional issue you likely need to do this in a variety of files each time which is tedious and time consuming.

### The chart users view

Initially chart users are faced with the same steep learning curve as the maintainers. They also need to be familiar with the underlying concepts to create a proper deployment configuration. This is worsened by the fact that each helm chart is basically a unique artifact with it's unique underlying implications of how it should be configured. Any more advanced user of Helm will be aware of the objects as they are represented by the Kubernetes API. But in order to specify the object with the properties they have in mind they need to understand the individual charts assumptions and the Helm machinery in the back. As an analogy, it is comparable to someone who wants to speak english (Kubernetes) being told he has to learn portugese (Helm) and all regional portugese dialects (actual Helm chart interfaces) to do so.

The best practices guidelines that are available do cover some ground to align chart writing and understanding but still leave most design aspects to the maintainers. From personal experience you almost always need to inspect the files in the `/templates` folder to learn about the effects of changing configuration parameters in the `values.yaml`. 

Additionally, depending on the requirements and preferences of the chart maintainer it is often the case that features required for a particular user are not implemented in the chart at all. To give an example of this, let's take a look at specifying `imagePullSecrets` for deployments within a helm chart:
- It might not be possible to specify them with the given chart in case the chart maintainers did not opt for implementing them, maybe being focused on public cloud deployments only. In this case you need to submit a pull requrest, modify locally, fork or something else to fulfill your requirement.
- The helm chart might have very different expectations on how they should be specified. Looking at some public helm charts available:
  - The `cerebro` helm chart at `https://github.com/helm/charts/blob/master/stable/cerebro/templates/deployment.yaml` requires you to specify `imagePullSecrets` as an array/list of values (excluding the `name` keys) per image:
  
    ```yaml
    {{- if .Values.image.pullSecrets }}
    imagePullSecrets:
    {{- range .Values.image.pullSecrets }}
    - name: {{ . }}
    {{- end }}
    {{- end }}
    ```
  - The `sonarqube` helm chart at `https://github.com/helm/charts/blob/master/stable/cerebro/templates/deployment.yaml` requires you to specify `imagePullSecrets` as a string. This means you can only specify one:
  
    ```yaml
    {{- if .Values.image.pullSecret }}
    imagePullSecrets:
    - name: {{ .Values.image.pullSecret }}
    {{- end }}
    ```

  - The `prometheus` helm chart at `https://github.com/helm/charts/blob/master/stable/prometheus/templates/deployments/alertmanager.yaml` however wants `imagePullSecrets` provided as an array of key-value pairs with repeated `name` keys:
  
    ```yaml
    {{- if .Values.imagePullSecrets }}
    imagePullSecrets:
    {{ toYaml .Values.imagePullSecrets | indent 2 }}
    {{- end }}
    ```

## Further remarks

There are various groups of people that work with Helm. There might be a group of people concerned with maintaining and installing a specific chart to the best of their effort. But there are also people who maintain and consume a larger number of charts which likely are overwhelmed by the various design approaches to creating Helm charts. Out of necessity, this group of people needs to get involved deeply in the design of individual helm charts to be able to understand how to configure them. By that point you are also likely familiar with the Kubernetes API and YAML structures and feel closer to using this than dissecting the many individual abstractions introduced by Helm charts. That is why HULL allows you to write regular Kubernetes YAMLs for the most part and only supports frequent usecases by the light abstraction layer it introduces.

This is where the HULL library chart can step in. It allows Helm chart maintainers to create sound charts with reduced effort in a streamlined way. You can lay out all the objects needed for your chart in a concise manner and allow more experienced users to change the default setup to their needs.

## Testing and installing a chart

To test or install a chart the standard Helm tooling is used. See also the Helm documentation at `https://helm.sh` 

- Helm v3:
  - Test a chart

    `<PATH_TO_HELM_V3_BINARY> template --debug --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> --output-dir <PATH_TO_OUTPUT_DIRECTORY> <PATH_TO_CHART_DIRECTORY>`

  - Install or upgrade a release: 

    `<PATH_TO_HELM_V3_BINARY> upgrade --install --debug --create-namespace --atomic --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> <RELEASE_NAME> <PATH_TO_CHART_DIRECTORY>`

## Creating and configuring chart

The tasks of creating and configuring a HULL based helm chart can be considered as two sides of the same coin. Both sides interact with the same  interface (the HULL library) to specify the objects that should be created. The task from a creators/maintainers perspective is foremeost to provide the ground structure for the objects that make up the particular application which is to be wrapped in a helm chart. The consumer of the chart is tasked with appropriately adding his system specific context to the ground structure wherein he has the freedom to change and even add objects as needed to achieve his goals. At deploy time the creators base structure is merged with the consumers system-specific yaml file to build the complete configuration. Interacting via the same library interface fosters common understanding of how to work with the library on both sides and can eliminate most of the tedious copy&paste creation and examination heavy configuration processes.

So all that is needed to create a helm chart based on HULL is a standard scaffolded helm chart directory structure. Add the HULL library chart as a subchart and configure the default objects to deploy via the `values.yaml` and you are done. There is no limit as to how many objects of whatever type you create for your products deployment.

But besides allowing to define complex objects and their relations with HULL you could also use it to wrap simple Kubernetes Objects you would otherwise either deploy via kubectl (being out of line from the management perspective with helm releases) or have to write a significant amnount of boilerplate to achieve this.

TODO: Create scaffold chart with each release 

The base structure of the `values.yaml` understood by HULL is given here in the next section. This essentially forms the single interface for producing and consuming HULL based charts. Any object is only created in case it is defined and enabled in the `values.yaml`, this means you might want to preconfigure objects for consumers that would just need to enable them if they want to use them.

## HULL interface defined in `values.yaml`

At the top level of the YAML structure, HULL distinguishes between `config` and `objects`. While the `config` subconfiguration is intended to deal with metadata and product specific settings, concrete objects to be rendered are specified under the `objects` key.

## _The `config` section_

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `config` | Specification of configuration options. <br><br>Has only the following sub-fields: <br><br>`specific`<br>`general` | |
| `config.general` | In this section you might define everything that is not particular to a unique product but to a range of products you want to deploy via helm. See the subfields descriptions for their inteded usage. <br><br>Has only the following sub-fields: <br><br>`rbac`<br>`data`<br>`metadata` | |
| `config.general.rbac` | Global switch which enables RBAC objects for installation. <br><br> If `true` the enabled objects are deployed to the cluster, if `false` no RBAC objects are created.<br><br> RBAC objects that are deployable are:<br>`serviceaccounts`<br>`roles`<br>`rolebindings`<br>`clusterroles`<br>`clusterrolebindings`  | `true` | `false` |
| `config.general.data` | Free form field whereas subfields of this field should have a clearly defined meaning in the context of your product suite. <br><br>For example, assume all of your products or microservices (each coming as a seperate helm chart) depends on the same given endpoints (authentication, configuration, ...). You might have a shared Kubernetes job executed by each helm chart which targets those endpoints. Now you could specify an external HULL `values.yaml` containing the job specification and the endpoint definition here in a way you see fit and construct an overlay `values.yaml` rendered on top of each deployment and have a unified mechanism in place.  | `{}` |
| `config.general.metadata` | Defined metadata fields here will be automatically added to all objects metadata. <br><br>Has only the following sub-fields: <br><br>`labels`<br>`annotations`| | 
| `config.general.metadata.labels` | Labels added to all objects. The `common` labels refer to the Kubernetes common labels and `custom` labels can be freely specified. <br><br>Has only the following sub-fields: <br><br>`common`<br>`custom`| | 
| `config.general.metadata.labels.common` | Common labels specification as defined in https://helm.sh/docs/chart_best_practices/labels/ and https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/. <br><br>Unless specifically overwriten with empty values (`''`) all metadata labels are automatically added to all objects according to their default definition. It should be considered to set a value for `config.general.metadata.labels.common.'app.kubernetes.io/part-of'` if the helm chart is part-of a product suite. | | 
| `config.general.metadata.labels.common.'app.kubernetes.io/managed-by'` | Managed by metadata. | `{{ .Release.Service }}` |
| `config.general.metadata.labels.common.'app.kubernetes.io/version'` | Version metadata. | `{{ .Chart.AppVersion }}` |
| `config.general.metadata.labels.common.'app.kubernetes.io/part-of'` | Part-of metadata. | `"unspecified"` |
| `config.general.metadata.labels.common.'app.kubernetes.io/name'` | Name metadata. | `{{ printf "%s-%s" .ChartName <hullObjectKey> }}`
| `config.general.metadata.labels.common.'app.kubernetes.io/instance'` | Instance metadata. | `{{ .Release.Name }}`
| `config.general.metadata.labels.common.'app.kubernetes.io/component'` | Component metadata. | `<hullObjectKey>`
| `config.general.metadata.labels.common.'helm.sh/chart'` | Helm metadata. | `{{ (printf "%s-%s" .Chart.Name .Chart.Version) | replace "+" "_" }}`
| `config.general.metadata.labels.custom` | All specified custom labels are automatically added to all objects of this helm chart. | `{}`| 
| `config.general.metadata.annotations` | All specified annotations are automatically added to all objects of this helm chart. | `{}`| 
| `config.general.metadata.nameOverride` | The name override is applied to values of metadata label `app.kubernetes.io/name`. If set this effectively replaces the chart name here.
| `config.general.metadata.fullnameOverride` | If set, the fullname override is applied to all object names and replaces the `<release>-<chart>` pattern in object names.
| `config.specific` | Free form field that holds configuration options that are specific to the specific product contained in the helm chart. Typically the values specified here ought to be used to populate the contents of configuration files that a particular applications read their configuration from at startup. Hence the `config.specific` fields are typically being consumed in ConfigMaps or Secrets. | `{}` | `maxDatepickerRange:`&#160;`50`<br>`defaultPoolColor:`&#160;`"#FB6350"`<br>`updateInterval:`&#160;`60000`

## _The `objects` section_

The top-level object types beneath `hull.objects` represent the most commonly Kubernetes object types you might want to create instances from without creating custom templates in the `/templates` folder. Further K8S object types can be added as needed to the library so it can easily be brought on par with a new Kubenetes releases. 

Some general remarks about the concepts behind rendering objects via the HULL library:

- for all top-level object types, instances of a particular type are always identified by a `<hullNameKey>` which is unique to the instance and object type combination. The same key can however be used for instances of different object types. The intention is to allow multi-layered merging by stacking `values.yaml` files on top of each other. You might start with defining the default object structure of the application or micro service defined in the given helm chart. Then you might add a `values.yaml` layer for a particular environment like staging or production. Then you might add a `values.yaml` layer for credentials. And so on. By uniquely identifying the instances of a particular K8s object type it becomes easy to adjust the objects properties through a multitude of layers.
- each particular instance can have an `enabled` sub-field set to `true` or `false`. This way you can predefine instances of object types in your helm charts `values.yaml` but not deploy them in a default scenario. Or enable them by default and refrain from deploying them in a particular environment by disabling them in an overlayed system specific `values.yaml`. Note that unless you explicitly specify `enabled: false` each instance you define will be created by default, a missing `enabled` key is equivalent to `enabled: true`.
- the `<hullNameKey>` of all instances is used for naming the instance. All instance names are constructed by the following ground rule: `{{ printf "%s-%s" .ReleaseName <hullObjectKey> }}`. This generates unique, dynamic names per object type and release + instance key combination. 

  Note that you can opt to define a static name for instances you create by adding a property `staticName: true` to your objects definition. If you do so the objects name will exactly match the key name you chose.
- cross-referencing objects within a helm chart is a useful feature of the HULL library. This is possible in the several contexts:
  -  when a reference to a ConfigMap or Secret comes into play you can just reference the `<hullConfigMapNameKey>` or `<hullSecretNameKey>` of the targeted instance and the dynamic name will be rendered in the output. this is possible for referencing 
     - a ConfigMap or Secret behind a Volume or 
     - a Secret behind an Ingress' TLS specification or
     - a ConfigMap or Secret behind an environment value added to a container spec.
  - when referencing Services in the backend of an ingress' host you can specify the `<hullServiceNameKey>` to reference the backend service   
- the K8s objects that can be created via HULL aim at supporting the full configuration options that the Kubernetes API provides for each object. In the description of each HULL wrapped object it is noted down which Kubernetes properties are not supported for configuration via HULL. The top level configuration properties are slightly adapted from the K8S API version to shorten the effort to create metadata.
- some lower level structures are also converted from the Kubernetes API array form to a dictionary form. This also enables more sophisticated merging of layers since arrays don't merge well, they only can be overwritten completely. Overwriting arrays however can make it hard to forget about elements that are contained in the default form of the array (you would need to know that they exist in the first place). In short, for a layered configuration approach without an endless amount of elements in arrays or dictionaries the dictionary is preferable for representing data since it offers a much better merging support.

Below is the specification of the objects you can create via the HULL library under the top level `hull` key:

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
|
| `objects` | Objects which are to be created within your helm chart are specified here. <br><br>Has only the following sub-fields: <br><br>`configmap`<br>`secret`<br>`registry`<br>`deployment`<br>`job`<br>`daemonset`<br>`statefulset`<br>`cronjob`<br>`serviceaccount`<br>`role`<br>`rolebinding`<br>`clusterrole`<br>`clusterrolebinding`<br>`storageclass`<br>`persistentvolume`<br>`persistentvolumeclaim`<br>`service`<br>`ingress`<br>`customresource`<br>`servicemonitor`|
| `objects.configmap`<br>`objects.secret` | Configurationwise ConfigMaps and Secrets are configured identically. The difference between ConfigMaps and Secrets is that the contents of Secrets are encoded whereas ConfigMap contents are not. Secrets are decrypted when mounted so for usage there exists no difference in terms of specifying them within HULL. To work with a `configmap` or `secret` you can either specify the contents inline in `values.yaml` or source them via an external file reference.<br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullConfigMapNameKey>` or `<hullSecretNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all ConfigMaps or Secrets respectively.<br><br>Value:<br>ConfigMap or Secret specification in the form of a `<hull.v1.VirtualFolder>`. See below for reference. | `{}`|
| `objects.registry` | Configuration of Docker Registry Secrets. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullRegistryNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Registry Secrets<br><br>Value:<br>Registry specification in the form of a `<hull.v1.Registry>`. See below for reference. | `{}`
| `objects.deployment`  | Configuration of Deployments. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullDeploymentNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Deployments<br><br>Value:<br>Deployment specification in the form of a `<hullDeploymentSpec>`. See below for reference. | `{}`
| `objects.job` | Configuration of Jobs. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullJobNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Jobs<br><br>Value:<br>Job specificationin in the form of a `<hullJobSpec>`. See below for reference.  | `{}`
| `objects.cronjob` | Configuration of CronJobs. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullCronJobNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all CronJobs<br><br>Value:<br>CronJob specificationin in the form of a `<hullCronJobSpec>`. See below for reference. | `{}`
| `objects.service` | Configuration of Services. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullServiceNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Services<br><br>Value:<br>Service specification in the form of a `<hull.v1.Service>`. See below for reference. | `{}`
| `objects.ingress` | Configuration of Ingresses. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressNameKey>` or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Ingresses<br><br>Value:<br>Ingress specification in the form of a `<hull.v1.Ingress>`. See below for reference. | `{}`
| `objects.customresourcedefinition` | Configuration of CustomResourceDefinitions (CRDs). <br>Note: This is deprecated with introduction of Helm 3's improved CRD handling!<br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullCustomResourceDefinitionNameKey>`<br><br>Value:<br>CRD specification in the form of a `<hullCustomResourceDefinitionSpec>`. See below for reference. | `{}`
| `objects.customresources` | Configuration of CustomResources (CRs). <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullCustomResourceNameKey>`<br><br>Value:<br>CR specification in the form of a `<hull.v1.CustomResource>`. See below for reference. | `{}`
| `objects.serviceAccount` | Configuration of Service Accounts. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullServiceAccountNameKey>`<br><br>Value:<br>Service Account specification in the form of a `<hullServiceAccountSpec>`. See below for reference. <br><br>Note:<br> By default a single service account with  `<hullServiceAccountNameKey>` `default` is created and configured for the deployments given that `objects.rbac` is set to `true`. | | 
| `objects.role` | Configuration of Roles. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullRoleNameKey>`<br><br>Value:<br>Role specification in the form of a `<hullRoleSpec>`. See below for reference. <br><br>Note:<br> By default a single role with  `<hullRoleNameKey>` `default` is created given that `objects.rbac` is set to `true`. | | 
| `objects.rolebinding` | Configuration of RoleBindings. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullRoleBindingNameKey>`<br><br>Value:<br>RoleBinding specification in the form of a `<hullRoleBindingSpec>`. See below for reference. <br><br>Note:<br> By default a single RoleBinding with  `<hullRoleBindingNameKey>` `default` is created and connects the ServiceAccount with `<hullServiceAccountNameKey>` `default` with the Role with `<hullRoleNameKey>` `default` given that `objects.rbac` is set to `true`.| | 
| `objects.clusterrole` | Configuration of ClusterRoles. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullClusterRoleNameKey>`<br><br>Value:<br>ClusterRole specification in the form of a `<hullRoleSpec>`. See below for reference. | | 
| `objects.clusterrolebinding` | Configuration of ClusterRoleBindings. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullClusterRoleBindingNameKey>`<br><br>Value:<br>ClusterRoleBinding specification in the form of a `<hullRoleBindingSpec>`. See below for reference. | | 
| `objects.servicemonitor` | Configuration of Prometheus ServiceMonitors. <br><br> Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullServiceMonitorBindingNameKey>`<br><br>Value:<br>ServiceMonitor specification in the form of a `<hull.v1.ServiceMonitor>`. See below for reference. | `{}`

## _The `<hullSpec>` objects_

### The `<hull.v1.VirtualFolder>`

Represents the structure that is shared for defining the content of virtual folder data. <br>All `<hull.v1.VirtualFolder>` objects are addressed by their unique `<hullConfigMapNameKey>` or `<hullSecretNameKey>` internally.<br><br>The `<hull.v1.VirtualFolder>` is used for values of: <br>`objects.configmaps`<br>`objects.secrets` <br> <br><br> The `<hull.v1.VirtualFolder>` has exclusively the following sub-fields: <br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br>`data`<br>`files`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the ConfigMap or Key is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `staticName` | Specifies whether the key of the `<hull.v1.VirtualFolder>` will be used as static name of the created object or not. <br>If the field does not exist or is set to `false`, a dynamically created fullname will be composed out of the key name and release and chartname prefixes.<br> For example, a ConfigMap with `<hullConfigMapNameKey>` `applicationData` will by default be uniquely named as `{{ printf "%s-%s-%s" .Chart.Name .Release.Name <hullConfigMapNameKey> }}`. With `staticName: true` the resulting name will just be `applicationData`. <br><br>Set `staticName: true` in case you want to create ConfigMaps or Secrets with a static name which can be directly referenced by external charts not aware of the dynamic name composition of the HULL library. | |
| `inlines` | Dictionary with Key-Value pairs. Can be used to specify ConfigMap or Secret contents inline in the `values.yaml`. <br><br>Key: <br>Unique `<hull.v1.VirtualFolderInlineKeyName>` related to parent object<br><br>Value: <br>The `<hull.v1.VirtualFolderInlineSpec>` of the mount. See below for reference.  | `{}`| `entryscript.sh:`<br>&#160;&#160;`data:`&#160;`|-`<br>&#160;&#160;&#160;&#160;`#!/bin/bash`<br>&#160;&#160;&#160;&#160;`echo 'hello'`<br>`readme.txt:`<br>&#160;&#160;`data:`&#160;`'Just a text'`
| `files` | Dictionary with Key-Value pairs. Can be used to include files sourced from external directories. <br><br>Key: <br>Unique `<hull.v1.VirtualFolderFileKeyName>` related to parent object<br><br>Value: <br>The `<hull.v1.VirtualFolderFileSpec>` of the file inclusion. See below for reference. | `{}`|  `settings.json:`<br>&#160;&#160;`path:`&#160;`'files/settings.json'`<br>`application.config:`<br>&#160;&#160;`path:`&#160;`'files/appconfig.yaml'`<br>&#160;&#160;`noTemplating: true`

### The `<hull.v1.VirtualFolderInlineSpec>`

Represents the structure that is shared for defining the content of virtual folder data sourced from inline YAML. <br><br>The `<hull.v1.VirtualFolderInlineSpec>` is used for values of: <br>`<hull.v1.VirtualFolder>.inlines`<br> <br><br> The `<hull.v1.VirtualFolderInlineSpec>` has exclusively the following sub-fields: <br>`data`
| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `data` | The actual data to store at `data.<hull.v1.VirtualFolderInlineKeyName>` in the ConfigMap or Secret | `{}`| 

### The `<hull.v1.VirtualFolderFileSpec>`

Represents the structure that is shared for defining the content of virtual folder data sourced from external files. <br><br>The `<hull.v1.VirtualFolderFileSpec>` is used for values of: <br>`<hull.v1.VirtualFolder>.files`<br> <br><br> The `<hull.v1.VirtualFolderFileSpec>` has exclusively the following sub-fields: <br>`path`<br>`noTemplating`
| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `path` | Path must be relative to the charts root path.<br> Files can contain templating expressions which are rendered by default, this can be disabled by setting `noTemplating: true` | `{}`|
| `noTemplating` | If `noTemplating` is specified and set to `true`, no templating expressions are rendered when the file content is processed. <br>This can be useful in case you need to handle files already containing Go or Jinja templating expressions which should not be handled by Helm but by the deployed application.<br>If `noTemplating: false` or the key `noTemplating` is missing, templating expressions will be processed by Helm when importing the file. | `{}`| 


### The `<hull.v1.Registry>`

Represents the structure that is shared for defining the content of Registry Secrets. <br>All `<hull.v1.Registry>` objects are addressed by their unique `<hullRegistryNameKey>` internally.<br><br>The `<hull.v1.Registry>` is used for values of: <br>`objects.registries` <br><br>Has exclusively the following sub-fields: <br>`enabled`<br>`annotations`<br>`labels`<br>`server`<br>`username`<br>`password`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Registry Secret is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `server` | Docker Registry host address      | `""` | 
| `username` | Docker Registry username      | `""` | 
| `password` | Docker Registry password      | `""` | 

### The `<hullDeploymentSpec>`

Represents the structure that is shared for defining the content of Deployments. <br>All `<hullDeploymentSpec>` objects are addressed by their unique `<hullDeploymentNameKey>` internally.<br><br><br>The `<hullDeploymentSpec>` is used for values of: <br>`objects.deployments` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`templateAnnotations`<br>`templateLabels`<br>`pod`<br>`replicas`<br>`strategy`<br>`progressDeadlineSeconds`<br>`minReadySeconds`<br>`revisionHistoryLimit`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Deployment is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `templateAnnotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template annotations<br><br>Value: <br>The actual annotation content to store      | `{}`
| `templateLabels`  | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template labels<br><br>Value: <br>The actual label content to store      | `{}`
| `pod`  | Specification of the Deployment Pod in the form of a `<hull.v1.Pod.Spec>`. See below for reference. | 
| `replicas`  | Number of desired pod instances of the Deployment. Defaults to `1`. | `1`  
| `strategy`  | Update strategy. See `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy` | The Kubernetes API default is applied.
| `progressDeadlineSeconds`  | Deadline of deployment progress. See `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#progress-deadline-seconds` | The Kubernetes API default is applied.   
| `minReadySeconds`  | After how many seconds the all containers must be running. See `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#min-ready-seconds`| The Kubernetes API default is applied.
| `revisionHistoryLimit`  | Number of revisions to keep. See `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#revision-history-limit`| The Kubernetes API default is applied.

### The `<hullJobSpec>`

Represents the structure that is shared for defining the content of Jobs. <br>All `<hullJobSpec>` objects are addressed by their unique `<hullJobNameKey>` internally.<br><br><br>The `<hullJobSpec>` is used for values of: <br>`objects.jobs` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`templateAnnotations`<br>`templateLabels`<br>`pod`<br>`backoffLimit`<br>`config`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Deployment is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `templateAnnotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template annotations<br><br>Value: <br>The actual annotation content to store      | `{}`
| `templateLabels`  | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template labels<br><br>Value: <br>The actual label content to store      | `{}`
| `pod`  | Specification of the Job Pod in the form of a `<hull.v1.Pod.Spec>`. See below for reference. | 
| `backoffLimit`  | Number of attempts to run the job until it completes successfully. See `https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup` | The Kubernetes API default is applied.
| `completions`  | Number of job overall completion. See `https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup` | The Kubernetes API default is applied.
| `activeDeadlineSeconds`  | Longest time in seconds the job is allowed to run. See `https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup` | The Kubernetes API default is applied.
| `parallelism`  | Number of parallel jobs. See `https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#parallel-jobs` | The Kubernetes API default is applied.

### The `<hullCronJobSpec>`

Represents the structure that is shared for defining the content of Cron Jobs. <br>All `<hullCronJobSpec>` objects are addressed by their unique `<hullCronJobNameKey>` internally.<br><br><br>The `<hullCronjobSpec>` is used for values of: <br>`objects.cronjobs` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`templateAnnotations`<br>`templateLabels`<br>`pod`<br>`schedule`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Deployment is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `templateAnnotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template annotations<br><br>Value: <br>The actual annotation content to store      | `{}`
| `templateLabels`  | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in Deployment template labels<br><br>Value: <br>The actual label content to store      | `{}`
| `pod`  | Specification of the CronJob Pod in the form of a `<hull.v1.Pod.Spec>`. See below for reference. | 
| `schedule`  | Schedule for the CronJob in cron format. See https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs | | `*/1 * * * *`

### The `<hull.v1.Pod.Spec>`

Represents the structure that is shared for defining the content of Pods. <br><br><br> The `<hull.v1.Pod.Spec>` is part of specifications for: <br>`<hullDeploymentSpec>`<br>`<hullJobSpec>`<br>`<hullCronJobSpec>` <br><br>Has exclusively the following sub-fields: <br><br>`restartPolicy`<br>`serviceAccountName`<br>`priorityClassName`<br>`affinity`<br>`tolerations`<br>`initContainers`<br>`containers`<br>`volumes`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `restartPolicy` | Restart Policy to use. <br>See: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy | The Kubernetes API default is applied.
| `serviceAccountName` | Name of ServiceAccount to use. If not configured explicitly the `objects.serviceaccounts.default` ServiceAccount is used in case it is enabled via `objects.rbac.enabled` and created as `objects.serviceaccounts.default`. If it is not enabled then the Kubernetes default ServiceAccount named "default" is used. | `objects.serviceaccounts.default` or `'default'`
| `priorityClassName` | Name of an existing PriorityClass to assign the pod. See: https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass | | `MostCriticalApps`
| `affinity` | Affinity settings for the pod. See: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity | `{}`| `podAntiAffinity:`<br>&#160;&#160;`preferredDuringSchedulingIgnoredDuringExecution:`<br>&#160;&#160;`- weight: 100`<br>&#160;&#160;&#160;&#160;&#160;&#160;`podAffinityTerm:`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`labelSelector:`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`topologyKey: "kubernetes.io/hostname"`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`matchExpressions:`:<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`- key: "app"`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`operator: In`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`values:`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`- vidispine-server`
| `tolerations` | Toleration settings for the pod. See: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#concepts | `[]`| `- key: "example-key"`<br>&#160;&#160;&#160;&#160;`operator: "Exists"`<br>&#160;&#160;&#160;&#160;`effect: "NoSchedule"`
| `initContainers` |  Dictionary with Key-Value pairs. <br><br>Key: <br>Unique `<hullInitContainerNameKey>` related to parent object or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all InitContainers of the parent object.<br><br>Value: <br>The `<hull.v1.Container>` of the init container. See below for reference. | `{}`| 
| `containers` |  Dictionary with Key-Value pairs. <br><br>Key: <br>Unique `<hullContainerNameKey>` related to parent object or `_HULL_OBJECT_TYPE_DEFAULT_` to provide defaults that should be applied to all Containers of the parent object.<br><br>Value: <br>The `<hull.v1.Container>` of the container. See below for reference. | `{}`| `mediaeditor:`<br>&#160;&#160;`image:`<br>&#160;&#160;&#160;&#160;`repository:`&#160;`codemill.azurecr.io/codemill/mediaeditor`<br>&#160;&#160;`ports:`<br>&#160;&#160;&#160;&#160;`http:`<br>&#160;&#160;&#160;&#160;&#160;&#160;`containerPort: 5000`<br>&#160;&#160;&#160;&#160;&#160;&#160;`protocol: TCP`<br>&#160;&#160;`resources:`<br>&#160;&#160;&#160;&#160;`limits:`<br>&#160;&#160;&#160;&#160;&#160;&#160;`cpu: 500m`<br>&#160;&#160;&#160;&#160;&#160;&#160;`memory: 1024Mi`<br>&#160;&#160;&#160;&#160;`requests:`<br>&#160;&#160;&#160;&#160;&#160;&#160;`cpu: 250m`<br>&#160;&#160;&#160;&#160;&#160;&#160;`memory: 512Mi`<br>&#160;&#160;&#160;&#160;`command:`<br>&#160;&#160;&#160;&#160;`- "/bin/bash"`<br>&#160;&#160;&#160;&#160;`args:`<br>&#160;&#160;&#160;&#160;`- "entrypoint.sh"`<br>&#160;&#160;&#160;&#160;`volumeMounts:`<br>&#160;&#160;&#160;&#160;&#160;&#160;`settings:`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`'/app/appsettings.json':`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`subPath: 'appsettings.json'`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`'/app/entrypoint.sh':`<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`subPath: 'entrypoint.sh'`
| `volumes` |  Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullVolumeNameKey>` related to parent object.<br><br>Value: <br>The `<hullVolumeSpec>` of the container. See below for reference. | `{}`| `licensesVolume:`<br>&#160;&#160;`secret:`<br>&#160;&#160;&#160;&#160;`name: licenses`<br>`config:`<br>&#160;&#160;`configMap:` <br>&#160;&#160;&#160;&#160;`name: config`<br>&#160;&#160;&#160;&#160;`defaultMode: '0744'`

### The `<hull.v1.Container>`

Represents the structure that is shared for defining the content of Containers. <br>All `<hull.v1.Container>` objects are addressed by their `<hull.v1.ContainerNameKey>` internally which is unique in relation to its parent object.<br><br> The `<hull.v1.Container>` is used for values of: <br>`<hull.v1.Pod.Spec>.initContainers`<br>`<hull.v1.Pod.Spec>.containers`<br><br>Has exclusively the following sub-fields: <br><br>`image`<br>`imagePullPolicy`<br>`ports`<br>`command`<br>`args`<br>`livenessProbe`<br>`readinessProbe`<br>`resources`<br>`env`<br>`mounts`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `image.repository` | Name/Repository of the container image | | `myregistry/videoeditor`
| `image.tag` | Tag of the container image | | `20.1.3-pre.321`
| `imagePullPolicy` | Defines when and how images are pulled. See: https://kubernetes.io/docs/concepts/containers/images/#updating-images | The Kubernetes API default is applied. | `IfNotPresent`| 
| `ports` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullPortNameKey>` related to parent object.<br><br>Value: <br>The `<hullContainerPortSpec>` of the port. See below for reference. | `{}`| 
| `command` | Command(s) to run the container with.<br> See: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/ | `[]` | `- "./entrypoint.sh"`
| `args` | Arguments for the command the container starts with.<br> See: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/ | `[]` | `- "-jar"`<br>`- "/opt/wildfly-swarm.jar"`<br>`- "-Dswarm.http.port=8080"`<br>`- "-c"`<br>`- "/opt/standalone.xml"`
| `livenessProbe` | Specification of the liveness probe.<br> See: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes | `{}` | `httpGet:`<br>&#160;&#160;`scheme: HTTP`<br>&#160;&#160;`path: /healthz`<br>&#160;&#160;`port: 8080`<br>`initialDelaySeconds: 15`<br>`timeoutSeconds: 1`
| `readinessProbe` | Specification of the readiness probe.<br> See: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes | `{}` | `httpGet:`<br>&#160;&#160;`scheme: HTTP`<br>&#160;&#160;`path: /healthz`<br>&#160;&#160;`port: 8080`<br>`initialDelaySeconds: 15`<br>`timeoutSeconds: 1`
| `resources` | Specification of the container resources.<br> See: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes | `{}` |`limits:`<br>&#160;&#160;`cpu: 500m`<br>&#160;&#160;`memory: 1024Mi`<br>`requests:`<br>&#160;&#160;`cpu: 250m`<br>&#160;&#160;`memory: 512Mi`
| `env` | Dictionary with Key-Value pairs. See: https://kubernetes.io/docs/concepts/containers/container-environment-variables. <br><br>Key: <br>Unique `name` of the  environment variable as `<hullEnvNameKey>` related to parent object.<br><br>Value: <br>The `<hullEnvSpec>` of the Environment Variable. See below for reference. | `{}`
| `mounts` | Dictionary with Key-Value pairs. See: https://kubernetes.io/docs/tasks/configure-pod-container/configure-volume-storage/<br><br>Key: <br>Unique `<hullMountNameKey>` of the mount related to parent object.<br><br>Value: <br>The `<hullMountSpec>` of the mount. See below for reference. | `{}`

### The `<hullMountSpec>`

Represents the structure that is shared for defining the content of mount specifications. The `<hullMountNameKey>` is equivalent to an existing `<hullVolumeNameKey>`.<br><br><br> The `<hullMountSpec>` is part of specifications for: <br>`<hull.v1.Container>`<br><br>Has exclusively the following sub-fields: <br><br>`volume`<br>`containerPath`<br>`volumeSubPath`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `volume` | The `<hullVolumeKeyName>` of the voume to mount from. | `{}` |  `licensesVolume:`<br>&#160;&#160;`'/etc/ssl/certs/':`<br>`config:`<br>&#160;&#160;`'/etc/nginx/conf.d/user.conf':`<br>&#160;&#160;&#160;&#160;`subPath: 'default_user'` 
| `volumeSubPath` | Optional limit to single subPath from source to mount | 
| `containerPath` | Path in the container to mount to. | 

### The `<hullContainerPortSpec>`

Represents the structure that is shared for defining the content of Container Port specifications. <br><br><br> The `<hullContainerPortSpec>` is part of specifications for: <br>`<hull.v1.Container>`<br><br>Has exclusively the following sub-fields: <br><br>`protocol`<br>`containerPort`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `protocol` | The protocol over which the containers port communicates | `TCP`| 
| `containerPort` | The port which the Container/Pod exposes to the cluster | | `8080`

### The `<hullEnvSpec>`

Represents the structure that is shared for defining the content of Environment Variable specifications. <br><br><br> The `<hullEnvSpec>` is part of specifications for: <br>`<hull.v1.Container>`<br><br>Has exclusively the following sub-fields: <br><br>`protocol`<br>`containerPort`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `value` | The concrete value of the environment variable. <br> Note: If set, any further `valueFromConfigMap` or `valueFromSecret` specification is ignored. |  | `Some Value`
| `valueFrom` | Specification that the value of the Environment Variable comes from another source. <br> Note: Only evaluated if no `value` specification is provided.<br><br>Has exclusively the following sub-fields: <br><br>`configMapKeyRef`<br>`secretKeyRef`| 
| `valueFrom.configMapKeyRef` | Specification of the ConfigMap reference for this Environment Variable. <br><br> Note: If set, any further `valueFrom.secretKeyRef` field is ignored. <br><br>Has exclusively the following sub-fields: <br><br>`name`<br>`staticName`<br>`key`| | `valueFrom:`<br>&#160;&#160;`configMapKeyRef:`<br>&#160;&#160;&#160;&#160;`name:`&#160;`config`<br>&#160;&#160;&#160;&#160;`key:`&#160;`default_user`
| `valueFrom.configMapKeyRef.name` | The `<hullConfigMapNameKey>` of the Configmap to refer to as source for Environment Variable if `staticName` evaluates to false. Otherwise the static name of the ConfigMap in the cluster sourcing this Environment Variable.  | 
| `valueFrom.configMapKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.configMapKeyRef` refers to a static name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.configMapKeyRef` shall reference a `<hullConfigMapNameKey>` defined in this helm chart. | |
| `valueFrom.configMapKeyRef.key` | The `data` key name holding the value contained in ConfigMap specified in `valueFrom.configMapKeyRef.name`. |
| `valueFrom.secretKeyRef` | Specification of the Secret reference for this Environment Variable. <br><br> Note: Only evaluated if no `value` or `valueFrom.configMapKeyRef` field is provided. <br><br>Has exclusively the following sub-fields: <br><br>`name`<br>`staticName`<br>`key`| | `valueFrom:`<br>&#160;&#160;`secretKeyRef:`<br>&#160;&#160;&#160;&#160;`name:`&#160;`config`<br>&#160;&#160;&#160;&#160;`key:`&#160;`default_user`
| `valueFrom.secretKeyRef.name` | The `<hullSecretNameKey>` of the Secret to refer to as source for Environment Variable if `staticName` evaluates to false. Otherwise the static name of the Secret in the cluster sourcing this Environment Variable.  | 
| `valueFrom.secretKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.secretKeyRef` refers to a static name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.secretKeyRef` shall reference a `<hullSecretNameKey>` defined in this helm chart. | |
| `valueFrom.secretKeyRef.key` | The `data` key name holding the value contained in Secret specified in `valueFrom.secretKeyRef.name`. |

### The `<hullVolumeSpec>`

Represents the structure that is shared for defining the content of Volumes. <br><br><br> The `<hullVolumeSpec>` is part of specifications for: <br>`<hull.v1.Pod.Spec>`<br><br>Has exclusively the following sub-fields: <br><br>`staticName`<br>`configMap`<br>`secret`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `configMap` | Presence of this key indicates that this Volume refers to a ConfigMap. <br> Note: If set, any further `secret` specification is ignored.<br>The different casing `configmap` is also supported but is deprecated and usage should be avoided! | | `configMap:` <br>&#160;&#160;`name: config`<br>&#160;&#160;`defaultMode:`&#160;`'0744'`
| `configMap.name` | The `<hullConfigMapNameKey>` of the Configmap to mount as a volume if `staticName` evaluates to false. Otherwise the static name of the ConfigMap in the cluster representing this Volume. | 
| `configMap.staticName` | Specifies whether the `name` key of this `<hullVolumeSpec>` refers to a static name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `<hullVolumeSpec>` shall reference a `<hullConfigMapNameKey>` defined in this helm chart. | |
| `configMap.defaultMode` | The default mode of the Configmap to mount as a volume. | 
| `secret` | Presence of this key indicates that this Volume refers to a Secret. <br> Note: Only evaluated if no `configMap` specification is provided. | | `secret:`<br>&#160;&#160;`name:`&#160;`licenses`
| `secret.name` | The `<hullSecretNameKey>` of the Secret to mount as a volume if `staticName` evaluates to false. Otherwise the static name of the Secret in the cluster representing this Volume. | 
| `secret.staticName` | Specifies whether the `name` key of this `<hullVolumeSpec>` refers to a static name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `<hullVolumeSpec>` shall reference a `<hullSecretNameKey>` defined in this helm chart. | |
| `secret.defaultMode` | The default mode of the Secret to mount as a volume. | 

### The `<hull.v1.Service>`

Represents the structure that is shared for defining the content of Services. <br>All `<hull.v1.Service>` objects are addressed by their unique `<hullServiceNameKey>` internally.<br><br>The `<hull.v1.Service>` is used for values of: <br>`objects.services` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`type`<br>`loadBalancerIP`<br>`externalName`<br>`ports`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Service is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `type` | The type of the service. See: https://kubernetes.io/docs/concepts/services-networking/service/ | The Kubernetes API default is applied. |
| `loadBalancerIP`  | IP of load balancer to communicate with.<br>Only relevant if `type: LoadBalancer` | 
| `externalName`  | External endpoint of service<br>Only relevant if `type: ExternalName` | 
| `ports` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullServicePortNameKey>` related to parent object.<br><br>Value: <br>The `<hullServicePortSpec>` of the port. See below for reference. | `{}`| 

### The `<hullServicePortSpec>`

Represents the structure that is shared for defining the content of Service Port specifications. <br><br><br> The `<hullServicePortSpec>` is part of specifications for: <br>`<hull.v1.Service>`<br><br>Has exclusively the following sub-fields: <br><br>`protocol`<br>`port`<br>`targetPort`<br>`nodePort`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `protocol` | The protocol over which the containers port communicates | `TCP`| 
| `port` | The port on which the service receives traffic | | `8080` 
| `targetPort` | The port which the service targets on the selected pods. | | `80`
| `nodePort`  | The port which is exposed on the node.<br>Only relevant if `type: NodePort`. | | `31011` 

### The `<hull.v1.Ingress>`

Represents the structure that is shared for defining the content of Ingresses. <br>All `<hull.v1.Ingress>` objects are addressed by their unique `<hullIngressNameKey>` internally. <br><br>The `<hull.v1.Ingress>` is used for values of: <br>`objects.ingresses` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`ingressClass`<br>`tls`<br>`hosts`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Ingress is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `ingressClass` | The class name of the ingress used for matching it with an ingress controller of same `ingressClass` | 
| `tls` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressTlsNameKey>` related to parent object.<br><br>Value: <br>The `<hullIngressTlsSpec>` of the certificate. See below for reference. | `{}`| 
| `rules` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressRuleNameKey>` related to parent object.<br><br>Value: <br>The `<hull.v1.Ingress.Rule>` of the host. See below for reference. | `{}`| 

### The `<hullIngressTlsSpec>`

Represents the structure that is shared for defining the content of TLS definitions. <br><br>The `<hullIngresTlsSpec>` is used for values of: <br>`<hull.v1.Ingress>.tls` <br><br>Has exclusively the following sub-fields: <br><br>`hosts`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `hosts` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressTlsHostsNameKey>` related to parent object.<br><br>Value: <br>The `<hullIngressTlsHostsSpec>` of the TLS host/secret combinations. See below for reference. | `{}`| 

### The `<hullIngressTlsHostsSpec>`

Represents the structure that is shared for defining the content of Ingress TLS host/certificate definitions. <br><br>The `<hullIngressTlsHostsSpec>` is used for values of: <br>`<hullIngressTlsSpec>.hosts` <br><br>Has exclusively the following sub-fields: <br><br>`hosts`<br>`secret`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `hosts` | Array of hosts contained in the `secret` certificate. | `[]` | 
| `secret` | Specification of the Secret containing the certificates. | `secret:`<br>&#160;&#160;`name:`&#160;`certs`
| `secret.name` | The `<hullSecretNameKey>` of the Secret to get certificates from if `staticName` evaluates to false. Otherwise the static name of the Secret in the cluster holding the certificates. | 
| `secret.staticName` | Specifies whether the `name` key of this `secret` refers to a static name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secret` shall reference a `<hullSecretNameKey>` defined in this helm chart. | |

### The `<hull.v1.Ingress.Rule>`

Represents the structure that is shared for defining the content of Ingress hosts definitions. <br><br>The `<hullIngresRuleSpec>` is used for values of: <br>`<hull.v1.Ingress>.rules` <br><br>Has exclusively the following sub-fields: <br><br>`host`<br>`http`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `host` | The DNS address of the host for which the ingress applies. Can be empty. | `{}` | 
| `http` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressRuleHttpNameKey>` related to parent object.<br><br>Value: <br>The `<hull.v1.Ingress.Rule.Spec>` of the `host`. See below for reference. | `{}`| 

### The `<hull.v1.Ingress.Rule.Spec>`

Represents the structure that is shared for defining the content of Ingress hosts definitions. <br><br>The `<hullIngresRuleHttpSpec>` is used for values of: <br>`<hull.v1.Ingress.Rule>` <br><br>Has exclusively the following sub-fields: <br><br>`path`<br>`pathType`<br>`backend`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `path` | The sub path path which is handled by this mapping  | |
| `pathType` | The path which is handled by this mapping  | |
| `backend` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullIngressRuleHttpBackendNameKey>` related to parent object.<br><br>Value: <br>The `<hullIngressRuleHttpBackendSpec>` of the `host`. See below for reference. | `{}`| 

### The `<hullIngressRuleHttpBackendSpec>`

Represents the structure that is shared for defining the content of Ingress hosts definitions. <br><br>The `<hullIngressRuleHttpBackendSpec>` is used for values of: <br>`<hullIngresRuleHttpSpec>.backend` <br><br>Has exclusively the following sub-fields: <br><br>`service`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `service` | The specification of the backend service who handles this path. <br><br>Has exclusively the following sub-fields: <br><br>`serviceName`<br>`servicePort` | |
| `service.serviceName` | The path which is handled by this mapping  | |
| `service.servicePort` | The path which is handled by this mapping  | |

### The `<hullCustomResourceDefinitionSpec>`

Represents the structure that is shared for defining the content of CustomResourceDefinitions (CRDs).<br><br>All `<hullCustomResourceDefinitionSpec>` objects are addressed by their unique `<hullCustomResourceDefinitionNameKey>` internally. <br><br>The `<hullCustomResourceDefinitionSpec>` is used for values of: <br>`objects.customresourcedefinitions` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`file`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the CRD deployment is enabled or not | |
| `file` | The path to a file whose contents are to be included as an CRD. CRD files need to be placed in the `crds` folder relative to the charts root path. <br> CRDs *cannot* contain templating expressions. | `{}`| `file:`&#160;`'voyager.appscode.com_certificates.yaml'`

### The `<hull.v1.CustomResource>`

Represents the structure that is shared for defining the content of CustomResources (CRs). <br><br>All `<hull.v1.CustomResource>` objects are addressed by their unique `<hullCustomResourceNameKey>` internally. <br><br>The `<hull.v1.CustomResource>` is used for values of: <br>`objects.customresources` <br><br>Has exclusively the following sub-fields: <br><br>`annotations`<br>`labels`<br>`enabled`<br>`apiVersion`<br>`kind`<br>`spec`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the CustomResource is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `apiVersion` | The API Version of the CR for which a matching CRD must exist in the system. | | `'voyager.appscode.com/v1beta1'`
| `kind` | The API kind of the CR for which a matching CRD must exist in the system. | | `'Certificates'`
| `spec` | The free-form spec of the CR which must follow the strucure given in the matching CRD. | | `'Certificates'`


### The `<hullServiceAccountSpec>`

Represents the structure that is shared for defining Service Accounts. <br><br>All `<hullServiceAccountSpec>` objects are addressed by their unique `<hullServiceAccountNameKey>` internally. <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the ServiceAccount is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`

### The `<hullRoleSpec>`

Represents the structure that is shared for defining `objects.roles` or `objects.clusterroles`. <br>All `<hullRoleSpec>` objects are addressed by their unique `<hullRoleNameKey>` or `<hullClusterRoleNameKey>` internally.<br><br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`rules`
| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the Role or ClusterRole is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `rules` | Rules to be associated with the Role or ClusterRole. | `[]` | `-`&#160;`apiGroups:`&#160;`['extensions']`<br>&#160;&#160;&#160;`resources:`&#160;`['podsecuritypolicies']`<br>&#160;&#160;&#160;`verbs:`&#160;`['use']`<br>&#160;&#160;&#160;`resourceNames:`&#160;`[resource]`

### The `<hullRoleBindingSpec>`

Represents the structure that is shared for defining `objects.rolebindings` or `objects.clusterrolebindings`. <br>All `<hullRoleBindingSpec>` objects are addressed by their unique `<hullRoleBindingNameKey>` or `<hullClusterRolebindingNameKey>` internally.<br><br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`roleRefName`<br>`roleRefKind`<br>`subjects`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the RoleBinding or ClusterRoleBinding is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `roleRefName` | Name of the object associated via the RoleBinding or ClusterRoleBinding. | | `default`
| `roleRefKind` | Kind of the object associated in the RoleBinding or ClusterRoleBinding. | | `Role`<br><br>or<br><br>`ClusterRole`
| `subjects` | Array of Subjects the RoleBinding or ClusterRoleBinding targets at in form of `<subjectSpec>`. | |  `-`&#160;`kind:`&#160;`ServiceAccount`<br>&#160;&#160;&#160;`name:`&#160;`myreleasedefault`<br>&#160;&#160;&#160;`namespace:`&#160;`myreleasenamespace`

### The `<hullSubjectSpec>`

Represents the structure that is shared for defining Subjects of RoleBindings or ClusterRoleBindings. <br>Has exclusively the following sub-fields: <br><br>`subjectName`<br>`subjectKind`<br>`subjectNamespace`
| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `subjectName` | The name of the subject. | | 
| `subjectKind` | The kind  of the subject | | `ServiceAccount`
| `subjectNamespace` | The namespace of the subject.<br><br> Note:<br>Not allowed for `RoleBinding` subjects because they are only valid per current namespace. | | `<release_namespace>`

### The `<hull.v1.ServiceMonitor>`

Represents the structure that is shared for defining the content of ServiceMonitors for Prometheus. <br><br>Note: This should only be used if Prometheus is deployed in the target system.<br><br>The `<hull.v1.ServiceMonitor>` is used for values of: <br>`objects.servicemonitors` <br><br>Has exclusively the following sub-fields: <br><br>`enabled`<br>`annotations`<br>`labels`<br>`endpoints`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `enabled` | Specifies whether the RoleBinding or ClusterRoleBinding is enabled for rendering or not. <br> If key is defined and set to `false` the object will not be rendered, otherwise it will.  | `true`|
| `annotations` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.annotations`. <br><br>Value: <br>The actual annotation content to store | `{}` | `importantAnnotation: "marked as legacy"`
| `labels` | Dictionary with Key-Value pairs.<br><br>Key: <br>Key for entry in `metadata.labels`<br><br>Value: <br>The actual label content to store | `{}` | `myApplicationLabel: "Great product!"`
| `endpoints` | Dictionary with Key-Value pairs.<br><br>Key: <br>Unique `<hullServiceMonitorEndpointNameKey>` related to parent object.<br><br>Value: <br>The `<hullServiceMonitorEndpointSpec>` of the Service Monitors Endpoint. See below for reference. | `{}`| 

### The `<hullServiceMonitorEndpointSpec>`

Represents the structure that is shared for defining the content of ServiceMonitors for Prometheus. <br><br>Note: This should only be used if Prometheus is deployed in the target system.<br><br>The `<hullServiceMonitorEndpointSpec>` is used for values of: <br>`<hull.v1.ServiceMonitor>.endpoints` <br><br>Has exclusively the following sub-fields: <br><br>`port`<br>`path`<br>`interval`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `port` | The port on which the service receives metric traffic. | | `http` 
| `path` | The path to the metrics endpoint in the service. | | `/metrics`
| `interval`  | The interval for polling the metrics from Prometheus. | | `30s` 