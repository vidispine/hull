# HULL: Helm Uniform Layer Library

> Abstractions need to be maintained - Kelsey Hightower

## Introduction

One major design aspect of [Helm](https://helm.sh) is that it forces the user to create individual abstractions of the Kubernetes configuration of applications. For each individual Helm Chart that is realized in form of YAML templates in a [Helm charts](https://helm.sh/docs/topics/charts/) `/templates` folder. These template files, containing boilerplate Kubernetes YAML code blocks on the one hand and custom configuration mappings utilizing Go Templating expressions on the other hand, provide the glue between the configuration of the application via the central `values.yaml` configuration file and the desired Kubernetes YAML output. Arguably this approach of per-application abstraction is suited well to create tailormade configuration packages for even the most specialized applications but comes at a cost of having a large overhead for simpler, recurring and off-the-shelf application packaging use cases. Creating, maintaining and (often) understanding the abstractions introduced by Helm Charts - especially when facing a high number of individual Helm charts from various sources - can become tedious and challenging.

The primary feature of the HULL library is the ability to remove customized YAML template files entirely from Helm chart workflows and thereby allowing to remove a level of abstraction. Using the HULL library chart, Kubernetes objects including all their properties can be completely and transparently specified in the `values.yaml`. The HULL library chart itself provides the uniform layer to streamline specification, configuration and rendering of Helm charts to achieve this. You can also think of it as a thin layer on top of the Kubernetes API to avoid the middleman between Helm Chart and Kubernetes API object configuration, yet providing flexibility when it is required to customize individual configuration options instead of requiring you to add each configuration switch manually to the templates. JSON schema validation based on the [Helm JSON validation feature](https://helm.sh/docs/topics/charts/#schema-files) (via `values.schema.json`) aids in writing Kubernetes API conforming objects right from the beginning when [using an IDE that supports live JSON schema validation](/hull/files/doc/json_schema_validation.md). Additional benefits (uniform inheritable object metadata, simplified inclusion of ConfigMaps/Secrets, cross-referencing values within the `values.yaml`, ...) are available with HULL which you can read about below in the **Key Features Overview**. But maybe most importantly, the HULL library can be added as a dependency to any existing Helm chart and be used side-by-side without breaking any existing Helm charts functionalities, see [adding the HULL library chart to a Helm chart](/hull/files/doc/setup.md) for more information. And lastly, by being a library chart itself, everything works 100% within the functionality that plain Helm offers - no additional tooling is introduced or involved.

### Versioning
HULL release versions are closely tied to Kubernetes release versions due to the incorporation of the release specific Kubernetes API schemas. Each HULL release branch therefore matches a Kubernetes release branch (such as `1.34`). Kubernetes patch releases provide non-breaking updates to a Kubernetes release while maintaining API stability and therefore play no role in the HULL versioning process. HULL's patch releases contain fixes and changes to HULL alone while maintaining compatibility to the Kubernetes releases API schema. 

HULLs compatibility with Helm matches the respective Kubernetes versions compatibility with Helm, see [Helm Version Support Policy for Helm 4](https://helm.sh/docs/topics/version_skew) and [Helm Version Support Policy for Helm 3](https://helm.sh/docs/v3/topics/version_skew) for the matching version ranges.

Each new release of HULL is thoroughly tested and, unless explicitly noted in the `CHANGELOG.md`, they do not contain breaking changes. Hence, it is usually safe to keep HULL versions up-to-date keeping compatibility with targeted Kubernetes cluster versions in mind.

### Helm v3 vs Helm v4

HULL remains compatible with existing Helm 3 releases and is fully compatible with Helm v4 starting with versions `1.34.2`, `1.33.3` and `1.32.6`. 

However, note that minor (however potentially chart-breaking) differences were introduced on the Helm side when moving to Helm v4:

- (technical) property names under the `Chart` object in the Helm root context have changed. This is with respect to capitalization of first letters mostly (eg. `maintainers` is now `Maintainers`), but for some properties capitalization is changed in multiple places (eg. `apiVersion` is now `APIVersion`).

- treatment of unset values has changed. To clarify what is mean with 'unset', consider property `field_unset` in this snippet:

  ```
  field_string: "some_text" # string text
  field_int: 123 # number
  field_bool: true # boolean
  field_unset: 
  field_dict: 
    key_1: value_1
  ```

  The behavior of Helm 3, when accessing such a field's property value, was to treat it as an empty string value from observation. This means, the key value pair exists in the `.Values` object tree and it's value is empty and of string type. With Helm 4 on the other hand, the field is absent from the object tree and accessing it will lead to an error.

Both aspects should typically be less relevant for HULL based charts, however it shall be documented here to avoid confusion. More detailed information can be found in the [related Helm issue](https://github.com/helm/helm/issues/31344).


**Your feedback on this project is valued, hence please comment or start a discussion in the `Issues` section or create feature wishes and bug reports. Thank you!**

The HULL library chart idea is partly inspired by the [common](
https://github.com/helm/charts/tree/master/incubator/common) Helm chart concept and for testing 

[![Gauge Badge](https://gauge.org/Gauge_Badge.svg)](https://gauge.org).

[![Build Status](https://dev.azure.com/arvato-systems-dmm/VPMS3%20CrossCutting/_apis/build/status/vidispine.hull?branchName=main)](https://dev.azure.com/arvato-systems-dmm/VPMS3%20CrossCutting/_build/latest?definitionId=589&branchName=main)

## Quick Start - the `hull-demo` chart

Before diving into the details of HULL, here is a first glimpse at how it works. You can simply download the latest version of the `hull-demo` Helm chart from the Releases section of this page, it has everything bootstrapped for testing out HULL or setting up a new Helm Chart based on HULL with minimal effort.  

The `hull-demo` chart wraps a fictional application `myapp` with a `frontend` and `backend` deployment and service pair. There is a config file for the server configuration that is mounted to the `backend` pods. The `frontend` pods need to know about the `backend` service address via environment variables. Moreover, the setup should by default be easily switchable from a `debug` setup (using a NodePort for accessing the frontend) to a production-like setup (using a ClusterIP service and an ingress). 


it renders out a set of objects based on above `values.yaml` containing:
- at
- jz

Every aspect of this configuration can be changed or overwritten at deployment time using additional `values.yaml` overlay files, for example:
- switching the overall configuration from and to `debug` mode by settings `debug: true` or `debug: false`
- adding resource definitions to the deployments
- setting hostname and path for the ingress 
- add further environment variables to pods
- change `myapp` ConfigMaps source values (`rate_limit` and `max_connections`) or overwrite it completely
- ...

All objects and logic was created with under a hundred lines of overall configuration code in the `hull-demo`'s `values.yaml`. You can test all of the above mentioned aspects or simply experiment by adding additional `values.yaml` overlay files to the `helm template` command above. For bootstrapping your own Helm chart, just empty the `values.yaml` configuration, rename the charts folder and `name` in `Chart.yaml` to whatever you want and you are ready to go. 

This is a first demo of how HULL could be used but there is a lot more functionality and supported use-cases. Check the key features and the detailed documentation for more information.

## Key Features Overview

As highlighted above, when included in a Helm chart the HULL library chart can take over the job of dynamically rendering Kubernetes objects from their given specifications from the `values.yaml` file alone. With YAML object construction deferred to the HULL library's Go Templating functions instead of custom YAML templates in the `/templates` folder you can centrally enforce best practices:

### Works without creating any YAML templates

Concentrate on what is needed to specify Kubernetes objects without having to add individual boilerplate YAML templates to your chart. This removes a common source of errors and maintenance from the regular Helm workflow. **To have the HULL rendered output conform to the Kubernetes API specification, a large number of unit tests validate the HULL rendered output against the Kubernetes API JSON schema.**

  For more details refer to the documentation on [JSON Schema Validation](/hull/files/doc/json_schema_validation.md).


### Directly specify any property of a Kubernetes object

For all Kubernetes object types supported by HULL, **full configurational access to the Kubernetes object types properties is directly available**. This relieves chart maintainers from having to add missing configuration options one by one and the Helm chart users from forking the Helm chart to add just the properties they need for their configuration. Only updating the HULL chart to a newer version with matching Kubernetes API version is required to enable configuration of properties added to Kubernetes objects meanwhile in newer API versions. The HULL charts are versioned to reflect the minimal Kubernetes API versions supported by them. 

   For more details refer to the documentation on [Architecture Overview](/hull/files/doc/architecture.md).

### Unified interface for defining and configuring Helm charts backed by JSON schema

The single interface of the HULL library is used to both create and configure objects in charts for deployment. This fosters the mutual understanding of chart creators/maintainers and consumers of how the chart actually works and what it contains. Digging into the `/templates` folder to understand the Helm charts implications is not required anymore. To avoid any misconfiguration, the interface to the library - the `values.yaml` of the HULL library - is fully JSON validated. **When using an IDE supporting live JSON schema validation (e.g. VSCode) you can get IDE guidance when creating the HULL objects.  Before rendering, JSON schema conformance is validated by the HULL library.**

  For more details refer to the documentation on [JSON Schema Validation](/hull/files/doc/json_schema_validation.md).

### Automatic and configurable metadata enrichment of Kubernetes objects

**Uniform and rich metadata is automatically attached to all objects created by the HULL library.** 

  - Kubernetes standard labels as defined for [Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) and [Helm](https://helm.sh/docs/chart_best_practices/labels/#standard-labels) are added to all objects metadata automatically. 
  - Additional custom labels and annotations metadata can be set hierarchically for:
    - all created Kubernetes objects or 
    - all created Kubernetes objects of a given type or 
    - a group of objects of different object types or
    - any individual Kubernetes object. 

  For more details on metadata overwriting refer to the advanced example below.

### Flexible and comfortable integration of ConfigMaps and Secrets into your Helm chart

Flexible handling of ConfigMap and Secret input by choosing between inline specification of contents in `values.yaml` or import from external files for contents of larger sizes. When importing data from files the data can be either run through the templating engine or imported un-templated 'as is' if it already contains templating expressions that shall be passed on to the consuming application. With a focus on convenient handling of standard scenarios, you can also define file contents as a regular YAML structure in the `values.yaml` and have HULL serialize it automatically to JSON or YAML by the file extension or explicily to any representation of your choice. HULL takes care of the Base64 encoding of Secrets so writing ConfigMaps and Secrets works the exact same way and **adding ConfigMaps or Secrets to your deployment requires only a few lines of code.**

  For more details refer to the documentation on [ConfigMaps and Secrets](/hull/files/doc/API/hull_objects_configmaps_secrets.md).

### Advanced defaulting capabilities to reduce unnecessary repetitions

Extensive defaulting capabilities for instantiating object instances. Whether you want to have all your object instances or groups of instances share certain aspects such as labels or annotations, container environment variables or mounted volumes, HULL provides support to efficiently define default values for object instance fields avoiding unnecessary configuration repetitions.

  For more details refer to the [Chart Design](/hull/files/doc/chart_design.md) advices.

### Run Go Templating functions directly in your `values.yaml`

For more complex scenarios where actual values in the target YAML are subject to configurations in the `values.yaml`, there is **support to dynamically populate values by injecting Go Templating expressions defined in place of the value in the `values.yaml`**. For example, if your concrete container arguments depend on various other settings in `values.yaml` you can inject the conditions into the calculation of the arguments or simply reference other fields in the `values.yaml`.

  For more details refer to the documentation on [Transformations](/hull/files/doc/transformations.md).

### Optional hashing of ConfigMaps and Secrets to foster pod restarts on content changes

Enable automatic hashing of referenced ConfigMaps and Secrets to facilitate pod restarts on changes of configuration when required.

  For more details refer to the documentation on [Pods](/hull/files/doc/API/hull_objects_pod.md).

To learn more about the general architecture and features of the HULL library see the [Architecture Overview](/hull/files/doc/architecture.md)

## Important information

Some important things to mention first before looking at the library in more detail:

⚠️ **While there may be several benefits to rendering YAML via the HULL library please take note that it is a non-breaking addition to your Helm charts. The regular Helm workflow involving rendering of YAML templates in the `/templates` folder is completely unaffected by integration of the HULL library chart. Sometimes you might have very specific requirements on your configuration or object specification which the HULL library does not meet so you can use the regular Helm workflow for them and the HULL library for your more standard needs - easily in parallel in the same Helm chart.** ⚠️

⚠️ **Note that a single static file, the `hull.yaml`, must be copied 'as-is' without any modification from an embedded HULL charts root folder to the parent charts `/templates` folder to be able to render any YAML via HULL. It contains the code that initiates the HULL rendering pipeline, see [adding the HULL library chart to a Helm chart](/hull/files/doc/setup.md) for more details!** ⚠️

⚠️ **At this time HULL releases are tested against all existing non-beta and non-alpha Helm 3 CLI versions. Note that Helm CLI versions `3.0.x` are not compatible with HULL, all other currently existing non-beta and non-alpha versions are compatible.** ⚠️

⚠️ **It is intended to support the latest 3 major Kubernetes releases with corresponding HULL releases. At this time Kubernetes versions `1.32` and `1.33` and `1.34` have a matching and maintained HULL release.** ⚠️

## NEW! The HULL Tutorials

If you like a hands on approach you are invited to take a look at the [new HULL tutorials series at dev.to](https://dev.to/gre9ory/series/18319)! The eigth part tutorial will start from the very beginning of setting up Helm and creating a HULL based chart to finalizing a real life HULL based Helm Chart step by step. To highlight the differences to the regular Helm chart workflow the tutorials take the popular [`kubernetes-dashboard`](https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard) Helm chart as a source and transport it to a functionally equivalent HULL based Helm chart. In the end it shows that reducing the lines of configuration to create and maintain can be reduced by more than 50% when using a HULL based approach instead of the regular Helm style of writing charts!

## Creating and configuring a HULL based chart

To get started on configuring your HULL based chart please refer to the [API documentation](/hull/files/doc/API). 

## Testing and installing a HULL based chart
To test or install a chart based on HULL the standard Helm v3 tooling is usable. See also the Helm documentation at the [Helm website](https://helm.sh). 

### Testing a HULL based chart

To inspect the outcome of a specific `values.yaml` configuration you can simply render the templates which would be deployed to Kubernetes and inspect them with the below command adapted to your needs:

  `<PATH_TO_HELM_V3_BINARY> template --debug --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> --output-dir <PATH_TO_OUTPUT_DIRECTORY> <PATH_TO_CHART_DIRECTORY>`

### Install or upgrade a release: 

Installing or upgrading a chart using HULL follows the standard procedures for every Helm chart:

  `<PATH_TO_HELM_V3_BINARY> upgrade --install --debug --create-namespace --atomic --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> <RELEASE_NAME> <PATH_TO_CHART_DIRECTORY>`


## First Examples

Using the nginx deployment example from the Kubernetes documentation https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment as something we want to create with our HULL based Helm chart:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
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

To render this analogously using the HULL library your chart needs to be [setup for using HULL](/hull/files/doc/setup.md). In the following section we assume the parent Helm chart is named `hull-test` and we use the `helm template` command to test render the `values.yaml`'s.

### Minimal Example

A minimal example of creating the expected result from above would be to create a `values.yaml` like below in your parent chart (commented with some explanations). Note that some default features of HULL such as RBAC and dynamic naming are explicitly disabled here to obtain the output matching the above example closely:

```yaml
hull:
  config:
    general:
      rbac: false # Don't render RBAC objects. By default HULL would provide 
                  # a 'default' Role and 'default' RoleBinding associated with 
                  # a 'default' ServiceAccount to use for all pods.
                  # You can modify this as needed. Here we turn it off to not 
                  # render the default RBAC objects.
  objects:
    serviceaccount:
      default:
        enabled: false # The release specific 'default' ServiceAccount created
                       # for a release by default is disabled here. In this case 
                       # it will not be rendered out and automatically used as 
                       # 'serviceAccountName' in the pod templates. 
    deployment:
      nginx: # all object instances have a key used for naming the objects and 
             # allowing to overwrite properties in multiple values.yaml layers
        staticName: true # forces the metadata.name to be just the <KEY> 'nginx' 
                         # and not a dynamic name '<CHART>-<RELEASE>-<KEY>' which 
                         # would be the better default behavior of creating 
                         # unique object names for all objects.
        replicas: 3
        pod:
          containers:
            nginx: # all containers of a pod template are also referenced by a 
                   # unique key to make manipulating them easy.
              image:
                repository: nginx
                tag: 1.14.2
              ports:
                http: # unique key per container here too. All key-value structures
                      # which are finally arrays in the K8S objects are converted to 
                      # arrays on rendering the chart.
                  containerPort: 80
```

This produces the following rendered deployment when running the `helm template` command (commented with some brief explanations):

```yaml
apiVersion: apps/v1 # derived from object type 'deployment'
kind: Deployment # derived from object type 'deployment'
metadata: 
  annotations: {}
  labels: # standard Kubernetes metadata is created always automatically.
    app.kubernetes.io/component: nginx 
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    helm.sh/chart: hull-test-1.31.0
  name: nginx # default name would be 'release-name-hull-test-nginx' 
              # but with staticName: true in the HULL spec it is just the key name
spec:
  replicas: 3
  selector: # selector is auto-created to match the unique metadata combination 
            # found also in the in the object's metadata labels.
    matchLabels:
      app.kubernetes.io/component: nginx
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations: {}
      labels: # auto-created metadata is added to pod template 
        app.kubernetes.io/component: nginx
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.31.0
        helm.sh/chart: hull-test-1.31.0
    spec:
      containers:
      - env: []
        envFrom: []
        image: nginx:1.14.2
        name: nginx
        ports:
        - containerPort: 80
          name: http # name 'http' derived from the key of the port 
                     # object defined in the values.yaml
        volumeMounts: []
      imagePullSecrets: {}
      initContainers: []
      volumes: []
```

### Advanced Example

Now to render the nginx deployment example showcasing extra features of the HULL library you can could create the below `values.yaml` file in your parent chart. Note that this is a very advanced example of what is possible using this library chart. 

This example highlights:

- hierarchical metadata handling
- default RBAC setup of objects
- dynamic naming mechanism
- transformations
- easy inclusion of ConfigMaps and/or Secrets

```yaml
hull:
  config:
    general:  # This time we are not setting rbac: false 
              # so RBAC default objects are created. 
              # If the default objects don't match the use-case
              # you can tweak all aspects individually if needed
      metadata:
        labels:         
          custom: # Additional labels added to all K8S objects
            general_custom_label_1: General Custom Label 1
            general_custom_label_2: General Custom Label 2
            general_custom_label_3: General Custom Label 3
        annotations: 
          custom: # Additional annotations added to all K8S objects
            general_custom_annotation_1: General Custom Annotation 1
            general_custom_annotation_2: General Custom Annotation 2
            general_custom_annotation_3: General Custom Annotation 3
    specific: # Put configuration options specific to this chart here
      nginx_tag: 1.14.2 # You can also use entries here to globally 
                        # define values that are referenced in multiple
                        # places in your chart. See how this field 
                        # is accessed below in the deployment.

  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_: # A special object key available for
                                  # all object types allowing defining 
                                  # defaults for properties of all object 
                                  # type instances created.
        annotations:  
          default_annotation_1: Default Annotation 1
          default_annotation_2: Default Annotation 2
          general_custom_annotation_2:  Default Annotation 2  # overwriting this 
                                                              # general annotation for
                                                              # all deployments
          
        labels:
          default_label_1: Default Label 1
          default_label_2: Default Label 2
          general_custom_label_2:  Default Label 2 # overwriting this 
                                                   # general label for
                                                   # all deployments
          
      nginx: # specify the nginx deployment under key 'nginx'
        # This time we're not setting the metadata.name to be static so 
        # name will be created dynamically and will be unique
        annotations:
          general_custom_annotation_3: Specific Object Annotation 3 # overwrite a
                                                                    # general annotation
          default_annotation_2: Specific Object Annotation 2 # overwrite a default annotation
          specific_annotation_1: Specific Object Annotation 1 # add a specific annotation 
                                                              # to the all this object's metadata
        labels: 
          general_custom_label_3: Specific Object Label 3 # overwrite a
                                                          # general label
          default_label_2: Specific Object Label 2 # overwrite a default label
          specific_label_1: Specific Object Label 1 # add a specific label 
                                                    # to the all this object's metadata
        templateAnnotations:
          specific_annotation_2: Specific Template Annotation 2 # this annotation will only appear 
                                                                # in the pod template metadata
        templateLabels:
          specific_label_2: Specific Template Label 2 # this label will only appear 
                                                      # in the pod template metadata
        replicas: 3
        pod:
          containers:
            nginx: # all containers of a pod template are also referenced by a 
                   # unique key to make manipulating them easy.
              image:
                repository: nginx
                tag: _HT!{{ (index . "$").Values.hull.config.specific.nginx_tag }}
                  # Applies a tpl transformation allowing to inject dynamic data based
                  # on values in this values.yaml into the resulting field (here the tag
                  # field of this container).
                  # In this case of simply retrieving a value, the same can be achieved 
                  # using a Get transformation like this:
                  #   _HT*hull.config.specific.nginx_tag
                  # _HT! is the short form of the transformation that applies tpl to
                  # a given value. This example just references the value of the field 
                  # which is specified further above in the values.yaml and will 
                  # produce 'image: nginx:1.14.2' when rendered in the resulting 
                  # deployment YAML but complex conditional Go templating logic is 
                  # applicable too. 
                  # There are some limitations to using this approach which are 
                  # detailed in the transformation.md in the doc section.
              ports:
                http: # unique key per container here too. All key-value structures
                      # which are array in the K8S objects are converted to arrays
                      # on rendering the chart.
                  containerPort: 80
    configmap: # this is to highlight the secret/configmap inclusion feature
      nginx_configmap: # configmap objects have keys too
        data: # specify for which contents a data entry shall be created
              # within only a few lines of configuration. Contents can come from ...
          an_inline_configmap.txt: # ... an inline specified content or ...
            inline: |- 
              Top secret contents
              spread over 
              multiple lines...
          contents_from_an_external_file.txt: # ... something from an external file.
            path: files/my_secret.txt 

```

This produces the following rendered objects when running the `helm template` command (commented with some brief explanations):

```yaml
---
# Source: hull-test/templates/hull.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    general_custom_annotation_1: General Custom Annotation 1 # All objects share the general_custom_annotations
    general_custom_annotation_2: General Custom Annotation 2 # if they are not overwritten for the object type's
    general_custom_annotation_3: General Custom Annotation 3 # default or specific instance
  labels:
    app.kubernetes.io/component: default
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    general_custom_label_1: General Custom Label 1 # All objects share the general_custom_labels
    general_custom_label_2: General Custom Label 2 # if they are not overwritten for the object type's
    general_custom_label_3: General Custom Label 3 # default or specific instance
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-default # This is the default ServiceAccount created for this chart.
                                       # As all object instances by default it will be assigned a 
                                       # dynamically created unique name in context of this object type.
                                       # In the simple example we disabled this rendering by 
                                       # setting enabled: false for this object's key.
---
# Source: hull-test/templates/hull.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  annotations:
    general_custom_annotation_1: General Custom Annotation 1
    general_custom_annotation_2: General Custom Annotation 2
    general_custom_annotation_3: General Custom Annotation 3
  labels:
    app.kubernetes.io/component: default
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    general_custom_label_1: General Custom Label 1
    general_custom_label_2: General Custom Label 2
    general_custom_label_3: General Custom Label 3
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-default # A default Role for RBAC. 
rules: []
---
# Source: hull-test/templates/hull.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  annotations:
    general_custom_annotation_1: General Custom Annotation 1
    general_custom_annotation_2: General Custom Annotation 2
    general_custom_annotation_3: General Custom Annotation 3
  labels:
    app.kubernetes.io/component: default
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    general_custom_label_1: General Custom Label 1
    general_custom_label_2: General Custom Label 2
    general_custom_label_3: General Custom Label 3
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-default
roleRef:
  apiGroup: rbac.authorization.k8s.io/v1
  kind: Role
  name: release-name-hull-test-default
subjects:
- apiGroup: rbac.authorization.k8s.io/v1
  kind: ServiceAccount
  name: release-name-hull-test-default # A default RoleBinding for RBAC. It connects the 
                                       # default ServiceAccount with the default Role.
                                       # By default RBAC is enabled in charts.
---
# Source: hull-test/templates/hull.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    default_annotation_1: Default Annotation 1 # non-overwritten default_annotation
    default_annotation_2: Specific Object Annotation 2 # overwritten default_annotation by instance
    general_custom_annotation_1: General Custom Annotation 1 # non-overwritten general_custom_annotation
    general_custom_annotation_2: Default Annotation 2 # overwritten general_custom_annotation 
                                                      # by default_annotation
    general_custom_annotation_3: Specific Object Annotation 3 # overwritten general_custom_annotation 
                                                              # by specific_annotation
    specific_annotation_1: Specific Object Annotation 1 # added annotation for instance metadata only
  labels:
    app.kubernetes.io/component: nginx
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    default_label_1: Default Label 1 # non-overwritten default_label
    default_label_2: Specific Object Label 2 # overwritten default_label by instance
    general_custom_label_1: General Custom Label 1 # non-overwritten general_custom_label
    general_custom_label_2: Default Label 2 # overwritten general_custom_label by default_label
    general_custom_label_3: Specific Object Label 3 # overwritten general_custom_label 
                                                    # by specific_label
    helm.sh/chart: hull-test-1.31.0
    specific_label_1: Specific Object Label 1 # added label for instance metadata only
  name: release-name-hull-test-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/component: nginx
      app.kubernetes.io/instance: release-name
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations:
        default_annotation_1: Default Annotation 1
        default_annotation_2: Specific Object Annotation 2
        general_custom_annotation_1: General Custom Annotation 1
        general_custom_annotation_2: Default Annotation 2
        general_custom_annotation_3: Specific Object Annotation 3
        specific_annotation_1: Specific Object Annotation 1
        specific_annotation_2: Specific Template Annotation 2 # this annotation was added only 
                                                              # for the pod template's metadata
      labels:
        app.kubernetes.io/component: nginx
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.31.0
        default_label_1: Default Label 1
        default_label_2: Specific Object Label 2
        general_custom_label_1: General Custom Label 1
        general_custom_label_2: Default Label 2
        general_custom_label_3: Specific Object Label 3
        helm.sh/chart: hull-test-1.31.0
        specific_label_1: Specific Object Label 1
        specific_label_2: Specific Template Label 2 # this label was added only 
                                                    # for the pod template's metadata
    spec:
      containers:
      - env: []
        envFrom: []
        image: nginx:1.14.2
        name: nginx
        ports:
        - containerPort: 80
          name: http
        volumeMounts: []
      imagePullSecrets: {}
      initContainers: []
      serviceAccountName: release-name-hull-test-default # the dynamically created name
      volumes: []
---
# Source: hull-test/templates/hull.yaml
apiVersion: v1
data:
  an_inline_configmap.txt: "Top secret contents\nspread over \nmultiple lines..."
  contents_from_an_external_file.txt: "Whatever was in this file ..."  
kind: ConfigMap
metadata:
  annotations:
    general_custom_annotation_1: General Custom Annotation 1 # All objects share the general_custom_annotations
    general_custom_annotation_2: General Custom Annotation 2 # if they are not overwritten for the object type's
    general_custom_annotation_3: General Custom Annotation 3 # default or specific instance
  labels:
    app.kubernetes.io/component: nginx_configmap
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: 1.31.0
    general_custom_label_1: General Custom Label 1 # All objects share the general_custom_labels
    general_custom_label_2: General Custom Label 2 # if they are not overwritten for the object type's
    general_custom_label_3: General Custom Label 3 # default or specific instance
    helm.sh/chart: hull-test-1.31.0
  name: release-name-hull-test-nginx_configmap
```

Read the additional documentation in the [documentation folder](/hull/files/doc) on how to utilize the features of the HULL library to the full effect.
