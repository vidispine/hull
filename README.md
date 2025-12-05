# HULL: Helm Uniform Layer Library

> Abstractions need to be maintained - Kelsey Hightower

## Introduction

One major design aspect of [Helm](https://helm.sh) is that it forces the user to create individual abstractions of the Kubernetes configuration of applications. For each individual Helm Chart that is realized in form of YAML templates in a [Helm charts](https://helm.sh/docs/topics/charts/) `/templates` folder. These template files, containing boilerplate Kubernetes YAML code blocks on the one hand and custom configuration mappings utilizing Go Templating expressions on the other hand, provide the glue between the configuration of the application via the central `values.yaml` configuration file and the desired Kubernetes YAML output. Arguably this approach of per-application abstraction is suited well to create tailormade configuration packages for even the most specialized applications but comes at a cost of having a large overhead for simpler, recurring and off-the-shelf application packaging use cases. Creating, maintaining and (often) understanding the abstractions introduced by Helm Charts - especially when facing a high number of individual Helm charts from various sources - can become tedious and challenging.

The primary feature of the HULL library is the ability to remove customized YAML template files entirely from Helm chart workflows and thereby allowing to remove a level of abstraction. Using the HULL library chart, Kubernetes objects including all their properties can be completely and transparently specified in the `values.yaml`. The HULL library chart itself provides the uniform layer to streamline specification, configuration and rendering of Helm charts to achieve this. You can also think of it as a thin layer on top of the Kubernetes API to avoid the middleman between Helm Chart and Kubernetes API object configuration, yet providing flexibility when it is required to customize individual configuration options instead of requiring you to add each configuration switch manually to the templates. JSON schema validation based on the [Helm JSON validation feature](https://helm.sh/docs/topics/charts/#schema-files) (via `values.schema.json`) aids in writing Kubernetes API conforming objects right from the beginning when [using an IDE that supports live JSON schema validation](doc/json_schema_validation.md). Additional benefits (uniform inheritable object metadata, simplified inclusion of ConfigMaps/Secrets, cross-referencing values within the `values.yaml`, ...) are available with HULL which you can read about below in the **Key Features Overview**. But maybe most importantly, the HULL library can be added as a dependency to any existing Helm chart and be used side-by-side without breaking any existing Helm charts functionalities, see [adding the HULL library chart to a Helm chart](doc/setup.md) for more information. And lastly, by being a library chart itself, everything works 100% within the functionality that plain Helm offers - no additional tooling is introduced or involved.

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

A bare default structure to capture these aspects may look like this (with added line comments for explanation):

```yaml
hull: # HULL is configured via subchart key 'hull'
  config: # chart setup takes place here for everything besides object definitions
    specific: # central place for shared values specific to this chart
      debug: true # a switch influencing creation of objects in this chart
      application_version: v23.1 # a shared image tag for multiple container
      myapp: # some exemplary configuration settings for the app, exposed here for transparency
        rate_limit: 100
        max_connections: 5
  objects: # all objects to create are defined here
    deployment: # create deployments
      myapp-frontend: # the base part of the object name for frontend deployment
        pod: # configure pod-related aspects
          containers: # non-init containers
            main: # one main container
              image: # provide image reference
                repository: mycompany/myapp-frontend # repository
                tag: _HT*hull.config.specific.application_version # reference to central tag value above
              ports: # exposed ports
                http: # port name is http
                  containerPort: 80 # the port number
              env: # environment variables
                SERVER_HOSTNAME: # name of variable
                  value: _HT^myapp-backend # value is dynamically rendered reference to myapp-backend service name
                SERVER_PORT: # name of variable
                  value: "8080" # backend service port
      myapp-backend: # the base part of the object name for backend deployment
        pod: # configure pod-related aspects
          containers: # non-init containers
            main: # one main container
              image: # image reference
                repository: mycompany/myapp-backend # repository
                tag: _HT*hull.config.specific.application_version # reference to central tag value above
              ports: # exposed ports
                http: # port name is http
                  containerPort: 8080 # the port number
              volumeMounts: # mounts of the container
                appconfig: # context key is appconfig
                  name: myappconfig # the name needs to match a volume
                  mountPath: /etc/config/appconfig.json # mountPath
                  subPath: backend-appconfig.json # subPath
          volumes: # volumes that may be mounted
            myappconfig: # key matching a volumeMounts name
              configMap: # configmap reference
                name: myappconfig # the configmap to load, simply referenced by key name   
    configmap: # create configmaps
      myappconfig: # the backend configuration
        data: # data section
          backend-appconfig.json: # key name is file name
            serialization: toPrettyJson # serialize the dictionary content of inline to pretty Json
            inline: # define the contents of the file as a dictionary for convenience
              rate-limit: _HT*hull.config.specific.myapp.rate_limit
              max-connections: _HT*hull.config.specific.myapp.max_connections
              debug-log: _HT!{{ if _HT*hull.config.specific.debug }}true{{ else }}false{{ end }}
    service: # create services
      myapp-frontend: # frontend service, automatically matches pods with identical parent object's key name
        ports: # definition of service ports
          http: # http port for type=ClusterIP
            enabled: _HT?not _HT*hull.config.specific.debug # bind rendering to debug: false condition, use embedded transformation to reference field
            port: 80 # regular port 
            targetPort: http # targetPort setting
          http_nodeport: # http port for type=NodePort
            enabled: _HT?_HT*hull.config.specific.debug # bind rendering to debug: true condition
            port: 80 # regular port 
            nodePort: 31111 # the node port
            targetPort: http # targetPort setting
        type: |-  # dynamically switch type based on hull.config.specific.debug setting
          _HT!
            {{- if _HT*hull.config.specific.debug -}}
            NodePort
            {{- else -}}
            ClusterIP
            {{- end -}}
      myapp-backend: # backend service, automatically matches pods with identical parent object's key name
        ports: # definition of service ports
          http: # http port
            port: 8080 # regular port 
            targetPort: http # targetPort setting
        type: ClusterIP # in cluster service
    ingress: # create ingresses
      myapp: # the central frontend ingress
        enabled: _HT?not _HT*hull.config.specific.debug # rendering bound to debug: false
        rules: # the ingress rules
          myapp: # key-value dictionary of rules
            host: SET_HOSTNAME_HERE # change the host at deployment time to actual one
            http: # http settings
              paths: # paths definition
                standard: # a standard path definition
                  path: / # could be changed at deployment time
                  pathType: ImplementationSpecific # path type
                  backend: # backend config
                    service: # service targeted
                      name: myapp-frontend # key name suffices to reference service created in this chart
                      port: # target port
                        name: http # target port name
```

This is the example constituting as `hull-demo`'s `values.yaml`, if you download the latest `hull-demo` release and execute:

```
helm template hull-demo-<version>.tgz
```

it renders out a set of objects based on above `values.yaml` containing:
- a deployment for `myapp-frontend` that has a centrally configured image `tag` set (by default `v23.1`), and environment variables pointing to the `myapp-backend`'s service in-cluster address
- a deployment for `myapp-backend` that has a centrally configured image `tag` set (by default `v23.1`) and a configuration mounted from the `myappconfig` ConfigMap
- a `myappconfig` ConfigMap with a JSON file that is dynamically built by incorporating templating expressions and referencing values defined elsewhere in `values.yaml`
- a simple ClusterIP Service fronting `myapp-backend` Deployment
- a service fronting `myapp-frontend` deployment whose type and port configuration is dependend on the central `debug` switch - either type `NodePort` in a `debug` setup mode or type `ClusterIP` in combination with a `myapp` ingress in non-debug setups
- an ingress object `myapp` which is only rendered/created in case the `debug: false` value is set

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

- Concentrate on what is needed to specify Kubernetes objects without having to add individual boilerplate YAML templates to your chart. This removes a common source of errors and maintenance from the regular Helm workflow. **To have the HULL rendered output conform to the Kubernetes API specification, a large number of unit tests validate the HULL rendered output against the Kubernetes API JSON schema.**

  For more details refer to the documentation on [JSON Schema Validation](doc/json_schema_validation.md).

- For all Kubernetes object types supported by HULL, **full configurational access to the Kubernetes object types properties is directly available**. This relieves chart maintainers from having to add missing configuration options one by one and the Helm chart users from forking the Helm chart to add just the properties they need for their configuration. Only updating the HULL chart to a newer version with matching Kubernetes API version is required to enable configuration of properties added to Kubernetes objects meanwhile in newer API versions. The HULL charts are versioned to reflect the minimal Kubernetes API versions supported by them. 

   For more details refer to the documentation on [Architecture Overview](doc/architecture.md).

- The single interface of the HULL library is used to both create and configure objects in charts for deployment. This fosters the mutual understanding of chart creators/maintainers and consumers of how the chart actually works and what it contains. Digging into the `/templates` folder to understand the Helm charts implications is not required anymore. To avoid any misconfiguration, the interface to the library - the `values.yaml` of the HULL library - is fully JSON validated. **When using an IDE supporting live JSON schema validation (e.g. VSCode) you can get IDE guidance when creating the HULL objects.  Before rendering, JSON schema conformance is validated by the HULL library.**

  For more details refer to the documentation on [JSON Schema Validation](doc/json_schema_validation.md).

- **Uniform and rich metadata is automatically attached to all objects created by the HULL library.** 
  - Kubernetes standard labels as defined for [Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) and [Helm](https://helm.sh/docs/chart_best_practices/labels/#standard-labels) are added to all objects metadata automatically. 
  - Additional custom labels and annotations metadata can be set hierarchically for:
    - all created Kubernetes objects or 
    - all created Kubernetes objects of a given type or 
    - a group of objects of different object types or
    - any individual Kubernetes object. 

  For more details on metadata overwriting refer to the advanced example below.

- Flexible handling of ConfigMap and Secret input by choosing between inline specification of contents in `values.yaml` or import from external files for contents of larger sizes. When importing data from files the data can be either run through the templating engine or imported un-templated 'as is' if it already contains templating expressions that shall be passed on to the consuming application. With a focus on convenient handling of standard scenarios, you can also define file contents as a regular YAML structure in the `values.yaml` and have HULL serialize it automatically to JSON or YAML by the file extension or explicily to any representation of your choice. HULL takes care of the Base64 encoding of Secrets so writing ConfigMaps and Secrets works the exact same way and **adding ConfigMaps or Secrets to your deployment requires only a few lines of code.**

  For more details refer to the documentation on [ConfigMaps and Secrets](doc/api/objects_configmaps_secrets.md).

- Extensive defaulting capabilities for instantiating object instances. Whether you want to have all your object instances or groups of instances share certain aspects such as labels or annotations, container environment variables or mounted volumes, HULL provides support to efficiently define default values for object instance fields avoiding unnecessary configuration repetitions.

  For more details refer to the [Chart Design](doc/chart_design.md) advices.

- For more complex scenarios where actual values in the target YAML are subject to configurations in the `values.yaml`, there is **support to dynamically populate values by injecting Go Templating expressions defined in place of the value in the `values.yaml`**. For example, if your concrete container arguments depend on various other settings in `values.yaml` you can inject the conditions into the calculation of the arguments or simply reference other fields in the `values.yaml`.

  For more details refer to the documentation on [Transformations](doc/transformations.md).

- Enable automatic hashing of referenced ConfigMaps and Secrets to facilitate pod restarts on changes of configuration when required.

  For more details refer to the documentation on [Pods](doc/api/objects_pod.md).

To learn more about the general architecture and features of the HULL library see the [Architecture Overview](doc/architecture.md)

## Important information

Some important things to mention first before looking at the library in more detail:

⚠️ **While there may be several benefits to rendering YAML via the HULL library please take note that it is a non-breaking addition to your Helm charts. The regular Helm workflow involving rendering of YAML templates in the `/templates` folder is completely unaffected by integration of the HULL library chart. Sometimes you might have very specific requirements on your configuration or object specification which the HULL library does not meet so you can use the regular Helm workflow for them and the HULL library for your more standard needs - easily in parallel in the same Helm chart.** ⚠️

⚠️ **Note that a single static file, the `hull.yaml`, must be copied 'as-is' without any modification from an embedded HULL charts root folder to the parent charts `/templates` folder to be able to render any YAML via HULL. It contains the code that initiates the HULL rendering pipeline, see [adding the HULL library chart to a Helm chart](doc/setup.md) for more details!** ⚠️

⚠️ **At this time HULL releases are tested against all existing non-beta and non-alpha Helm 3 CLI versions. Note that Helm CLI versions `3.0.x` are not compatible with HULL, all other currently existing non-beta and non-alpha versions are compatible.** ⚠️

⚠️ **It is intended to support the latest 3 major Kubernetes releases with corresponding HULL releases. At this time Kubernetes versions `1.32` and `1.33` and `1.34` have a matching and maintained HULL release.** ⚠️

## NEW! The HULL Tutorials

If you like a hands on approach you are invited to take a look at the [new HULL tutorials series at dev.to](https://dev.to/gre9ory/series/18319)! The eigth part tutorial will start from the very beginning of setting up Helm and creating a HULL based chart to finalizing a real life HULL based Helm Chart step by step. To highlight the differences to the regular Helm chart workflow the tutorials take the popular [`kubernetes-dashboard`](https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard) Helm chart as a source and transport it to a functionally equivalent HULL based Helm chart. In the end it shows that reducing the lines of configuration to create and maintain can be reduced by more than 50% when using a HULL based approach instead of the regular Helm style of writing charts!

## Creating and configuring a HULL based chart

The tasks of creating and configuring a HULL based helm chart can be considered as two sides of the same coin. Both sides interact with the same interface (the HULL library) to specify the objects that should be created. The task from a creators/maintainers perspective is foremost to provide the ground structure for the objects that make up the particular application which is to be wrapped in a Helm chart. The consumer of the chart is tasked with appropriately adding his system specific context to the ground structure wherein he has the freedom to change and even add or delete objects as needed to achieve his goals. At deploy time the creators base structure is merged with the consumers system-specific yaml file to build the complete configuration. Interacting via the same library interface fosters common understanding of how to work with the library on both sides and can eliminate most of the tedious copy&paste creation and examination heavy configuration processes.

So all that is needed to create a helm chart based on HULL is a standard scaffolded helm chart directory structure. Add the HULL library chart as a sub-chart, copy the `hull.yaml` from the HULL library chart to your parent Helm charts `/templates` folder. Then just configure the default objects to deploy via the `values.yaml` and you are done. There is no limit as to how many objects of which type you create for your deployment package.

But besides allowing to define more complex applications with HULL you could also use it to wrap simple Kubernetes Objects you would otherwise either deploy via kubectl (being out-of-line from the management perspective with helm releases) or have to write a significant amount of Helm boilerplate templates to achieve this. 

The base structure of the `values.yaml` understood by HULL is given here in the next section. This essentially forms the single interface for producing and consuming HULL based charts. Any object is only created in case it is defined and enabled in the `values.yaml`, this means you might want to pre-configure objects for consumers that would just need to enable them if they want to use them.

At the top level of the YAML structure, HULL distinguishes between `config` and `objects`. While the `config` sub-configuration is intended to deal with chart specific settings such as metadata and product settings, the concrete Kubernetes objects to be rendered are specified under the `objects` key.
An additional third top level key named `version` is allowed as well, when this is being set to the HULL charts version for example during the parent Helm Charts release pipeline it will automatically populate the label `vidispine.hull/version`on all objects indicating the HULL version that was used to render the objects.

### _The `config` section_

Within the `config` section you can configure general settings for your Helm chart. It is divided into two subsections, `config.general` and `config.specific`. 

### _The `config.general` section_

In contrast to the `config.specific` section, which should be populated with arbitrary data that is specific only to a single helm chart, the `config.general` section should be used to define everything that is not particular to a unique application. On the one hand it holds configuration options which are relevant for all HULL based charts but also leaves room under the `config.general.data` entry to define your own data fields which ideally are modeled the same way in other helm charts. For example, if several applications in a product suite depend on the same endpoints, you could model these endpoints uniformly under the `general.data` property in all relevant charts and thereby having your helm charts interface in the same way with e.g. a continuous deployment pipeline.

<br><br>`config.general` has only the following sub-fields: <br><br>`nameOverride`<br>`fullnameOverride`<br>`namespaceOverride`<br>`noObjectNamePrefixes`<br>`createImagePullSecretsFromRegistries`<br>`globalImageRegistryServer`<br>`globalImageRegistryToFirstRegistrySecretServer`<br>`debug`<br>`rbac`<br>`data`<br>`serialization`<br>`postRender`<br>`errorChecks`<br>`metadata`

| Parameter                       | Description                                                     | Default                      |                  Example |
| ------------------------------- | ----------------------------------------------------------------| -----------------------------| -----------------------------------------|
| `nameOverride` | The name override is applied to values of metadata label `app.kubernetes.io/name`. If set this effectively replaces the chart name here.
| `fullnameOverride` | If set to a value, the fullname override is applied as a prefix to all object names and replaces the standard `<release>-<chart>` prefix pattern in object names. |  | `myapp` |
| `namespaceOverride` | If set to a value, the namespace of all created objects is set to this value. If this is not defined, the namespace of all object instances defaults to the release namespace provided to the respective helm command. |  | `my-namespace` |
| `noObjectNamePrefixes` | If set, the object instance keys directly serve as the names for the Kubernetes objects created and are never prefixed. This is technically equivalent to setting `staticName` true on each object. Note that by setting this to `true` the value of `config.general.fullnameOverride` becomes irrelevant. | `false` | `true` |
| `createImagePullSecretsFromRegistries` | If true, image pull secrets are created from all registries defined in this Helm chart and are added to all pods. | `true` | `false` |
| `globalImageRegistryServer` | If not empty the `registry` field of all container `image` fields is set to the value given here. The setting of `config.general.globalImageRegistryToFirstRegistrySecretServer` is ignored if this field is non-empty. All defined explicit `registry` settings for an `image` are overwritten with this value.<br><br>Intended usage of this is to conveniently have all images pulled from a central docker registry in case of air-gap like deployment scenarios. <br><br>Contrary to setting `globalImageRegistryToFirstRegistrySecretServer` to `true`, in this case the registry secret is typically defined outside of this helm chart and the registry secret's server is referenced by its name directly. If you use this feature and define the Docker registry secret outside of this Helm chart you may additionally need to add `imagePullSecrets` to your pods in case the referenced Docker registry is not insecure. | `""` | `mycompany.docker-registry.io`
| `globalImageRegistryToFirstRegistrySecretServer` | If true and `globalImageRegistryServer` is empty, the `registry` field of all container `image` fields is set to the `server` field of the first found `registry` object. Note that this is the registry with the lowest alphanumeric key name if you provide multiple `registry` obejcts. Should normally be used together with setting `createImagePullSecretsFromRegistries` to `true` to benefit from autopopulated `imagePullSecrets` and accordingly set `registry`. Explicit `registry` settings for an `image` are overwritten with this value.<br><br>Intended usage of this setting is to conveniently have all images pulled from a central docker registry in case of air-gap like deployment scenarios.  | `false` | `true`
| `errorChecks` |<br><br>Options that determine in which cases HULL will generate an error on `helm install` or `helm template`. For more details see also the detailed documentation on [configuring error checks](doc/error_checking.md) <br><br>Has only the following sub-fields: <br><br>`objectYamlValid`<br>`hullGetTransformationReferenceValid`<br>`containerImageValid`<br>`virtualFolderDataPathExists`<br>`virtualFolderDataInlineValid`
| `errorChecks.objectYamlValid` | Validate that no broken YAML is rendered | `true`
| `errorChecks.hullGetTransformationReferenceValid` | Validate that all `_HT*` references point to an existing key in the `values.yaml` | `true`
| `errorChecks.containerImageValid` | Validate that all `pod`'s `containers` and `initContainers` `image` sections exist and have at least a `repository` set | `true`
| `errorChecks.virtualFolderDataPathExists` | Validate that all files being refered to in a ConfigMap and Secret's `data` `path` field do physically exist | `true`
| `errorChecks.virtualFolderDataInlineValid` | Validate that no `null` values or missing values (which are converted to empty strings) are set for ConfigMap and Secret's `data` `inline` fields | `false`
| `debug` |<br><br>Options that can help with debugging chart problems. Mostly obsolete and replaced by speaking default error messages configured under `errorChecks`.<br><br>Has only the following sub-fields: <br><br>`renderBrokenHullGetTransformationReferences`<br>`renderNilWhenInlineIsNil`<br>`renderPathMissingWhenPathIsNonExistent`
| `debug.renderBrokenHullGetTransformationReferences` | Global switch which if enabled will print out a string: <br><br>`HULL failed with error BROKEN-HULL-GET-TRANSFORMATION-REFERENCE: Element <y> in path <x.y.z> was not found `<br><br> including the `_HT*/hull.util.transformation.get` reference (`x.y.z`) and the missing key (`y`) if the transformation references a non existing dictionary key. This is useful to debug chart rendering and reduces searching for broken references because normally the installation aborts with an error on broken references (which may make it hard to pin point the problematic reference(s)). <br><br> <b>NOTE: <br><br>By now any broken get reference will be signaled by a speaking helm error by default so this switch is mostly obsolete for debugging broken references. It is recomended to disable this option and fail hard on broken get references instead and analyze problems directly from the error message.</b>| `false` | `true` |
| `debug.renderNilWhenInlineIsNil` | Global switch which if enabled will print out a string: <br><br>`<nil>`<br><br> as a `data` fields value when an `inline` spec references a `nil` pointer in a ConfigMap or Secret. If set to false, the `nil` value will be printed as an empty string in the ConfigMap or Secret `data` field. <br><br> <b>NOTE: <br><br>By now any invalid inline fields will be signaled by a speaking helm error by default (meaning `hull.config.general.errorChecks.virtualFolderDataInlineValid` is `true`). Enabling this switch is mostly obsolete for debugging and it is recomended to disable this option and fail hard on invalid inline fields.| `false` | `true` |
| `debug.renderPathMissingWhenPathIsNonExistent` | Global switch which if enabled will print out a string: <br><br>`<path missing: the_missing_path>`<br><br> in a ConfigMap or Secret `data` fields value including the `the_missing_path` value which does not resolve to a file. If false, the `data` fields value will resolve to an empty string. <br><br> <b>NOTE: <br><br>By now any non-existent file referenced in a path field will be signaled by a speaking helm error by default (meaning `hull.config.general.errorChecks.virtualFolderDataPathExists` is `true`). Enabling this switch is mostly obsolete for debugging and it is recomended to disable this option and fail hard on non-existing file path references. | `false` | `true` |
| `render` | Options to influence how HULL renders out objects as YAML.<br><br>Has only the following sub-fields: <br><br>`emptyAnnotations`<br>`emptyLabels`<br>`emptyHullObjects`|  |  |
| `render.emptyAnnotations` | If `true`, HULL renders out `annotations: {}` if no annotations exist for an object, if `false` the `annotations` key is omitted. | `false` | `true`
| `render.emptyLabels` | If `true`, HULL renders out `labels: {}` if no labels exist for an object, if `false` the `labels` key is omitted. | `false` | `true`
| `render.emptyTemplateAnnotations` | If `true`, HULL renders out `annotations: {}` in the `template` of a pod if no annotations exist for an object, if `false` the `annotations` key is omitted. | `false` | `true`
| `render.emptyTemplateLabels` | If `true`, HULL renders out `labels: {}` in the `template` of pods ` if no labels exist for an object, if `false` the `labels` key is omitted. | `false` | `true`
| `render.emptyHullObjects` | If `true`, HULL renders out arrays as empty arrays if no elements exist for some fields processed by HULL. If false, the key-value pair is ommited. <br><br> This affects fields which are mapped from a dictionary in HULL configuration to a Kubernetes array in the rendered YAML. The following is a list of affected fields in HULL's object configuration:<br><br><ul><li>`data` in `secret` and `configmap` objects</li><li>`initContainers`, `containers`, `volumes` and `imagePullSecrets` in `cronjob`,`daemonset`, `deployment`, `job` and `statefulset` `pod` objects</li><li>`ports`, `env`, `envFrom` and `volumeMounts` in `initContainers`, `containers` and `volumes` in `cronjob`,`daemonset`, `deployment`, `job` and `statefulset` `pod` objects</li><li>`ports` in `service` objects</li><li>`rules` and `tls` in `ingress` objects</li><li>`http.paths` in `rules` in `ingress` objects</li><li>`webhooks` in `validatingwebhookconfiguration` and `mutatingwebhookconfiguration`</li><li>`rules` in `clusterrole` and `role`</li>| `false` | `true`
| `postRender` | After HULL has fully rendered an object it is possible to manipulate the resulting YAML string. Possibilities to do so are provided as `postRender` actions here. <br><br><b>WARNING: Use with caution as this may corrupt the YAML structure!</b> |  |  |
| `postRender.globalStringReplacements` | A dictionary of replacement possibilities that may be applied to the rendered object's YAML. The main use case for this is in combination with extensive defaulting in `_HULL_OBJECT_TYPE_DEFAULT_` and `sources` object instances where it allows to inject instance specific strings into the defaulted YAML. Also, for down stream content that needs to preserve double curly braces as used in templating expressions, it allows to replace custonmizable placeholders with double curly opening and closing braces. The preconfigured mappings provided may be `enabled: true` on demand. Each mapping consists of following fields:<ul><li>`enabled`: execute mapping if `true`</li><li>`string`: the exact string part to be replaced</li><li>`replacement`: the type of value inserted instead of `string`. Can be one of the following static values `OBJECT_INSTANCE_KEY`, `OBJECT_INSTANCE_KEY_RESOLVED` and `OBJECT_INSTANCE_NAME` which are interpreted and resolved as explained below. Any other value is treated as a string value.
| `postRender.globalStringReplacements.instanceKey` | If `enabled`, the `string` value will be replaced with the actual object's `instance_key` as in `hull.objects.<object_type>.<instance_key>`. The value of `replacement` is `OBJECT_INSTANCE_KEY` for this mapping.  | `instanceKey:`<br>&#160;&#160;`enabled:`&#160;`false`<br>&#160;&#160;`string:`&#160;`_HULL_OBJECT_TYPE_DEFAULT_`<br>&#160;&#160;`replacement:`&#160;`OBJECT_INSTANCE_KEY` |
| `postRender.globalStringReplacements.instanceKeyResolved` | If `enabled`, the `string` value will be replaced with the actual object's `instance_key` as in `hull.objects.<object_type>.<instance_key>` or by `hull.objects.<object_type>.<instance_key>.metadataNameOverride` if this is defined. The value of `replacement` is `OBJECT_INSTANCE_KEY_RESOLVED` for this mapping. | `instanceKeyResolved:`<br>&#160;&#160;`enabled:`&#160;`false`<br>&#160;&#160;`string:`&#160;`_HULL_OBJECT_TYPE_DEFAULT_`<br>&#160;&#160;`replacement:`&#160;`OBJECT_INSTANCE_KEY_RESOLVED`
| `postRender.globalStringReplacements.instanceName` | If `enabled`, the `string` value will be replaced with the actual object's rendered `metadata.name`. The value of `replacement` is `OBJECT_INSTANCE_NAME` for this mapping. | `instanceName:`<br>&#160;&#160;`enabled:`&#160;`false`<br>&#160;&#160;`string:`&#160;`_HULL_OBJECT_TYPE_DEFAULT_`<br>&#160;&#160;`replacement:`&#160;`OBJECT_INSTANCE_NAME`
| `postRender.globalStringReplacements.openingDoubleCurlyBraces` | If `enabled`, the `string` value (default `{+{`) will be replaced with opening double curly braces `{{`. The value of `replacement` is thus `{{` for this mapping. | `openingDoubleCurlyBraces:`<br>&#160;&#160;`enabled:`&#160;`false`<br>&#160;&#160;`string:`&#160;`{+{`<br>&#160;&#160;`replacement:`&#160;`{{`
| `postRender.globalStringReplacements.closingDoubleCurlyBraces` | If `enabled`, the `string` value (default `}+}`) will be replaced with closing double curly braces `}}`. The value of `replacement` is thus `}}` for this mapping. | `closingDoubleCurlyBraces:`<br>&#160;&#160;`enabled:`&#160;`false`<br>&#160;&#160;`string:`&#160;`}+}`<br>&#160;&#160;`replacement:`&#160;`}}`
| `serialization` | General serialization options. | 
| `serialization.configmap.enabled` | If `enabled`, the mapped file extensions under `fileExtensions` are serialized with the given serialization method by default. If the `data` key ends with one of the mapped extensions the serialization method in the value is used to write the content to string. A specific `serialization` field on a configmaps `data` entry overwrites any default settings. | `true`
| `serialization.configmap.fileExtensions` | A dictionary of mappings from file extensions to serialization methods. | `fileExtensions:`<br>&#160;&#160;`json:`&#160;`toPrettyJson`<br>&#160;&#160;`yaml:`&#160;`toYaml`<br>&#160;&#160;`yml:`&#160;`toYaml`
| `serialization.secret.enabled` | If `enabled`, the mapped file extensions under `fileExtensions` are serialized with the given serialization method by default. If the `data` key ends with one of the mapped extensions the serialization method in the value is used to write the content to string. A specific `serialization` field on a secrets `data` entry overwrites any default settings. | `true`
| `serialization.secret.fileExtensions` | A dictionary of mappings from file extensions to serialization methods. | `fileExtensions:`<br>&#160;&#160;`json:`&#160;`toPrettyJson`<br>&#160;&#160;`yaml:`&#160;`toYaml`<br>&#160;&#160;`yml:`&#160;`toYaml`
| `config.general.rbac` | Global switch which enables RBAC objects for installation. <br><br> If `true` all enabled RBAC objects are deployed to the cluster, if `false` no RBAC objects are created at all.<br><br> RBAC objects that are deployable are:<br>`roles`<br>`rolebindings`<br>`clusterroles`<br>`clusterrolebindings`  | `true` | `false` |
| `config.general.data` | Free form field whereas subfields of this field should have a clearly defined meaning in the context of your product suite. <br><br>For example, assume all of your products or microservices (each coming as a separate helm chart) depends on the same given endpoints (authentication, configuration, ...). You might have a shared Kubernetes job executed by each helm chart which targets those endpoints. Now you could specify an external HULL `values.yaml` containing the job specification and the endpoint definition here in a way you see fit and construct an overlay `values.yaml` rendered on top of each deployment and have a unified mechanism in place.  | `{}` |
| `config.general.metadata` | Defined metadata fields here will be automatically added to all objects metadata. <br><br>Has only the following sub-fields: <br><br>`labels`<br>`annotations`| | 
| `config.general.metadata.labels` | Labels that are added to all objects. The `common` labels refer to the Kubernetes and Helm common labels and `custom` labels can be freely specified. <br><br>Has only the following sub-fields: <br><br>`common`<br>`custom`| | 
| `config.general.metadata.labels.common` | Common labels specification as defined in https://helm.sh/docs/chart_best_practices/labels/ and https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/. <br><br>Unless specifically overwritten with empty values (`''`) all metadata labels are automatically added to all objects according to their default definition. It should be considered to set a value for `config.general.metadata.labels.common.'app.kubernetes.io/part-of'` if the helm chart is part-of a product suite. | | 
| `config.general.metadata.labels.common.'app.kubernetes.io/managed-by'` | Managed by metadata. | `{{ .Release.Service }}` |
| `config.general.metadata.labels.common.'app.kubernetes.io/version'` | Version metadata. | `{{ .Chart.AppVersion }}` |
| `config.general.metadata.labels.common.'app.kubernetes.io/part-of'` | Part-of metadata. | `"unspecified"` |
| `config.general.metadata.labels.common.'app.kubernetes.io/name'` | Name metadata. | `{{ printf "%s-%s" .ChartName <hullObjectKey> }}`
| `config.general.metadata.labels.common.'app.kubernetes.io/instance'` | Instance metadata. | `{{ .Release.Name }}`
| `config.general.metadata.labels.common.'app.kubernetes.io/component'` | Component metadata. | `<hullObjectKey>`
| `config.general.metadata.labels.common.'helm.sh/chart'` | Helm metadata. | `{{ (printf "%s-%s" .Chart.Name .Chart.Version) | replace "+" "_" }}`
| `config.general.metadata.labels.custom` | All specified custom labels are automatically added to all objects of this helm chart. | `{}`| 
| `config.general.metadata.annotations` | Annotations that are added to all objects. The `custom` labels can be freely specified. <br><br>Has only the following sub-fields: <br><br>`custom`. | 
| `config.general.metadata.annotations.custom` | All specified custom annotations are automatically added to all objects of this helm chart. | `{}`| 
| `config.specific` | Free form field that holds configuration options that are specific to the specific product contained in the helm chart. Typically the values specified here ought to be used to populate the contents of configuration files that a particular applications read their configuration from at startup. Hence the `config.specific` fields are typically being consumed in ConfigMaps or Secrets. | `{}` | `maxDatepickerRange:`&#160;`50`<br>`defaultPoolColor:`&#160;`"#FB6350"`<br>`updateInterval:`&#160;`60000`

### _The `objects` section_

The top-level object types beneath `hull.objects` represent the supported Kubernetes object types you might want to create instances from. Each object type is a dictionary where the entries values are the objects properties and each object has it's own key which is unique to the object type it belongs to. Further K8S object types can be added as needed to the library so it can easily be extended. 

#### _Keys of object instances_

One important aspect is that for all top-level object types, instances of a particular type are always identified by a key which is unique to the instance and object type combination. The same key can however be used for instances of different object types.

By having keys that identify instances you can:

- do multi-layered merging of object properties by stacking `values.yaml` files on top of each other. You might start with defining the default object structure of the application or micro service defined in the given helm chart. Then you might add a `values.yaml` layer for a particular environment like staging or production. Then you might add a `values.yaml` layer for credentials. And so on. By uniquely identifying the instances of a particular K8s object type it becomes easy to adjust the objects properties through a multitude of layers.
- use the key of an instance for naming the instance. All instance names are constructed by the following ground rule: `{{ printf "%s-%s-%s" .Release.Name .Chart.Name key }}`. This generates unique, dynamic names per object type and release + instance key combination. 

  For example, assuming the parent Helm chart is named `my_webservice` and the release named `staging` and given this specification in `values.yaml`:

  ```yaml
  hull:
    objects:
      deployment:
        nginx:
          pod:
            containers:
              nginx:
                repository: nginx
                tag: 1.14.2
  ```

  a Kubernetes deployment object with the following `metadata.name` is created:

  `my_webservice-staging-nginx`

  > Note that you can opt to define a static name for instances you create by adding a property `staticName: true` to your objects definition. If you do so the objects name will exactly match the key name you chose.

- each particular instance can have an `enabled` sub-field set to `true` or `false`. This way you can predefine instances of object types in your helm charts `values.yaml` but not deploy them in a default scenario. Or enable them by default and refrain from deploying them in a particular environment by disabling them in an superimposed system specific `values.yaml`. Note that unless you explicitly specify `enabled: false` each instance you define will be created by default, a missing `enabled` key is equivalent to `enabled: true`.

- cross-referencing objects within a helm chart by the instance key is a useful feature of the HULL library. This is possible in these contexts:
  -  when a reference to a ConfigMap or Secret comes into play you can just use the key of the targeted instance and the dynamic name will be rendered in the output. This is possible for referencing 
    - a ConfigMap or Secret behind a Volume or 
    - a Secret behind an Ingress' TLS specification or
    - a ConfigMap or Secret behind an environment value added to a container spec.
  - when referencing Services in the backend of an ingress' host you can specify the key to reference the backend service.
  
  > Note that you can in these cases opt to refer to a static name instead too. Adding a property `staticName: true` to the dictionary with your reference will force the referenced objects name to exactly match the name you entered.

#### _Values of object instances_

The values of object instance keys reflects the Kubernetes objects to create for the chart. To specify these objects efficiently, the available properties for configuration can be split into three groups:

1. Basic HULL object configuration with [hull.ObjectBase.v1](doc/object_base.md) whose properties are available for all object types and instances. These are `enabled`, `staticName`, `annotations` and `labels`. 

    Given the example of a `deployment` named `nginx` you can add the following properties of [hull.ObjectBase.v1](doc/object_base.md) to the object instance:

    ```yaml
    hull:
      objects:
        deployment:
          nginx: # unique key/identifier of the deployment to create
            staticName: true # property of hull.ObjectBase.v1
                             # forces the metadata.name to be just the <KEY> 'nginx' 
                             # and not a dynamic name '<CHART>-<RELEASE>-<KEY>' which 
                             # would be the better default behavior of creating 
                             # unique object names for all objects.
            enabled: true    # property of hull.ObjectBase.v1
                             # this deployment will be rendered to a YAML object if enabled
            labels:
              demo_label: "demo" # property of hull.ObjectBase.v1
                                 # add all labels here that shall be added 
                                 # to the object instance metadata section
            annotations:
              demo_annotation: "demo" # property of hull.ObjectBase.v1
                                      # add all annotations here that shall be added 
                                      # to the object instance metadata section
            pod: 
              ... # Here would come the hull.PodTemplate.v1 definition
                  # see below for details

    ```

2. Specialized HULL object properties for some object types. Below is a reference of which object type supports which special properties in addition to the basic object configuration. 

    Again given the example of a `deployment` named `nginx` you would want to add properties of the HULL [**hull.PodTemplate.v1**](doc/api/objects_pod.md) to the instance. With them you set the `pod` property to define the pod template (initContainers, containers, volumes, ...) and can add `templateLabels` and `templateAnnotations` just to the pods created `metadata` and not the deployment objects `metadata` section:

    ```yaml
    hull:
      objects:
        deployment:
          nginx: 
            staticName: true 
            enabled: true 
            labels: 
              demo_label: "demo" 
            annotations: 
              demo_annotation: "demo" 
            templateLabels: # property of hull.PodTemplate.v1 to define 
                            # labels only added to the pod
              demo_pod_label: "demo pod" 
            templateAnnotations: # property of hull.PodTemplate.v1 to define 
                            # annotations only added to the pod
              demo_pod_annotation: "demo pod"
            pod: # property of hull.PodTemplate.v1 to define the pod template
              containers:
                nginx: # all containers of a pod template are also referenced by a 
                      # unique key to make manipulating them easy.
                  image:
                    repository: nginx # specify repository and tag
                                      # separately with HULL for easier composability
                    tag: 1.14.2
                  ... # further properties (volumeMounts, affinities, ...)

    ```
3. Kubernetes object properties. For each object type it is basically possible to specify all existing Kubernetes properties. In case a HULL property overwrites a identically named Kubernetes property the HULL property has precedence. Even if a HULL property overrides a Kubernetes property it is intended to provide the same complete configuration options, even if sometimes handled differently by HULL. 

    Some of the typical top-level Kubernetes object properties and fields don't require setting them with HULL based objects because they can be deducted automatically:
    - the `apiVersion` and `kind` are determined by the HULL object type and Kubernetes API version and don't require to be explicitly set (except for objects of type `customresource`).
    - the top-level `metadata` dictionary on objects is handled by HULL via the `annotations` and `labels` fields and the naming rules explained above. So the `metadata` field does not require configuration and is hence not configurable for any object. 

    Some lower level structures are also converted from the Kubernetes API array form to a dictionary form or are modified to improve working with them. This also enables more sophisticated merging of layers since arrays don't merge well, they only can be overwritten completely. Overwriting arrays however can make it hard to forget about elements that are contained in the default form of the array (you would need to know that they existed in the first place). In short, for a layered configuration approach without an endless amount of elements the dictionary is preferable for representing data since it offers a much better merging support.

    So again using the example of a `deployment` named `nginx` you can add the remaining available Kubernetes properties to the object instance which are not handled by HULL as shown below. For a `deployment` specifically you can add all the remaining properties defined in the `deploymentspec` API schema from [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#deploymentspec-v1-apps) which are `minReadySeconds`, `paused`, `progressDeadlineSeconds`, `replicas`, `revisionHistoryLimit` and `strategy`. If properties are marked as mandatory in the Kubernetes JSON schema you must provide them otherwise the rendering process will fail:

    ```yaml
    hull:
      objects:
        deployment:
          nginx: 
            staticName: true 
            enabled: true 
            labels: 
              demo_label: "demo" 
            annotations: 
              demo_annotation: "demo" 
            pod:
              ... # Here would come the hull.PodTemplate.v1 definition
                  # see above for details 
            replicas: 3 # property from the Kubernetes API deploymentspec
            strategy: # property from the Kubernetes API deploymentspec
              type: Recreate
            ... # further Kubernetes API deploymentspec options

    ```

#### _Composing objects with HULL_

Here is an overview of which top level properties are available for which object type in HULL. The HULL properties are grouped by the respective HULL JSON schema group they belong to. A detailed description of these groups and their properties is found in the documentation of this helm chart and the respective linked documents.

**[Workloads APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-workloads-apis-strong-)**

HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`deployment` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/api/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#deploymentspec-v1-apps)<br>`minReadySeconds`<br>`paused`<br>`progressDeadlineSeconds`<br>`replicas`<br>`revisionHistoryLimit`<br>`strategy` 
`job` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/api/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**jobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#jobspec-v1-batch)<br>`activeDeadlineSeconds`<br>`backoffLimit`<br>`completionMode`<br>`completions`<br>`manualSelector`<br>`parallelism`<br>`selector`<br>`suspend`<br>`ttlSecondsAfterFinished` 
`daemonset` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/api/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**daemonsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#daemonsetspec-v1-apps)<br>`minReadySeconds`<br>`ordinals`<br>`revisionHistoryLimit`<br>`updateStrategy` 
`statefulset` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/api/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**statefulsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#statefulsetspec-v1-apps)<br>`podManagementPolicy`<br>`replicas`<br>`revisionHistoryLimit`<br>`serviceName`<br>`updateStrategy`<br>`serviceName`<br>`volumeClaimTemplates` 
`cronjob` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Job.v1**](./README.md)<br>`job` | [**cronjobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#cronjobspec-v1-batch)<br>`concurrencyPolicy`<br>`failedJobsHistoryLimit`<br>`schedule`<br>`startingDeadlineSeconds`<br>`successfulJobsHistoryLimit`<br>`suspend` 

**[Service APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-service-apis-strong-)**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`endpoints`<br>(deprecated<br>since<br>K8S 1.33) | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**endpoints-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#endpoints-v1-core)<br>`subsets`
`endpointslice` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**endpointslice-v1-discovery-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#endpointslice-v1-discovery-k8s-io)<br>`addressType`<br>`endpoints`<br>`ports`
`service` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Service.v1**](doc/api/objects_service.md)<br>`ports` | [**servicespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#servicespec-v1-core)<br>`allocateLoadBalancerNodePorts`<br>`clusterIP`<br>`clusterIPs`<br>`externalIPs`<br>`externalName`<br>`externalTrafficPolicy`<br>`healthCheckNodePort`<br>`internalTrafficPolicy`<br>`ipFamilies`<br>`ipFamilyPolicy`<br>`loadBalancerClass`<br>`loadBalancerIP`<br>`loadBalancerSourceRanges`<br>`publishNotReadyAddresses`<br>`selector`<br>`sessionAffinity`<br>`sessionAffinityConfig`<br>`topologyKeys`<br>`type`
`ingress` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Ingress.v1**](doc/api/objects_ingress.md)<br>`tls`<br>`rules` | [**ingressspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#ingressspec-v1-networking-k8s-io)<br>`defaultBackend`<br>`ingressClassName`
`ingressclass` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ingressclassspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#ingressclassspec-v1-networking-k8s-io)<br>`controller`<br>`parameters`

**[Config and Storage APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-config-and-storage-apis-strong-)**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`configmap` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](doc/api/objects_configmaps_secrets.md)<br>`data` |  [**configmap-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#configmap-v1-core)<br>`binaryData`<br>`immutable`
`secret` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](doc/api/objects_configmaps_secrets.md)<br>`data` |  [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#secret-v1-core)<br>`immutable`<br>`stringData`<br>`type` 
`registry` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Registry.v1**](doc/api/objects_registry.md)<br>`server`<br>`username`<br>`password` | [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#secret-v1-core)
`persistentvolumeclaim` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumeclaimspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#persistentvolumeclaimspec-v1-core)<br>`accessModes`<br>`dataSource`<br>`resources`<br>`selector`<br>`storageClassName`<br>`volumeMode`<br>`volumeName`
`storageclass` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**storageclass-v1-storage-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#storageclass-v1-storage-k8s-io)<br>`allowVolumeExpansion`<br>`allowedTopologies`<br>`mountOptions`<br>`parameters`<br>`provisioner`<br>`reclaimPolicy`<br>`volumeBindingMode`

**[Metadata APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-metadata-apis-strong-)**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`customresource` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.CustomResource.v1**](doc/api/objects_customresource.md)<br>`apiVersion`<br>`kind`<br>`spec`
`limitrange` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**limitrange-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#limitrange-v1-core)<br>`limits`
`horizontalpodautoscaler` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.HorizontalPodAutoscaler.v1**](doc/api/objects_horizontalpodautoscaler.md)<br>`scaleTargetRef` | [**horizontalpodautoscalerspec-v2-autoscaling**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#horizontalpodautoscalerspec-v2-autoscaling)<br>`behavior`<br>`maxReplicas`<br>`metrics`<br>`minReplicas`
`mutatingwebhookconfiguration` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.MutatingWebhook.v1**](doc/api/objects_base_webhook.md)<br>`webhooks`
`poddisruptionbudget` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**poddisruptionbudgetspec-v1-policy**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#poddisruptionbudgetspec-v1-policy)<br>`maxUnavailable`<br>`minAvailable`<br>`selector`<br>`unhealthyPodEvictionPolicy`
`validatingwebhookconfiguration` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.ValidatingWebhook.v1**](doc/api/objects_base_webhook.md)<br>`webhooks` 
`priorityclass` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**priorityclass-v1-scheduling-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#priorityclass-v1-scheduling-k8s-io)<br>`description`<br>`globalDefault`<br>`preemptionPolicy`<br>`value`

**[Cluster APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-cluster-apis-strong-)**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`clusterrole` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Rule.v1**](doc/api/objects_role.md)<br>`rules` |  [**clusterrole-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#clusterrole-v1-rbac-authorization-k8s-io)<br>`aggregationRule`
`clusterrolebinding` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**clusterrolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#clusterrolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects`
`namespace` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**namespace-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#namespace-v1-core)<br>`spec`<br>`status`
`persistentvolume` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#persistentvolumespec-v1-core)<br>`accessModes`<br>`awsElasticBlockStore`<br>`azureDisk`<br>`azureFile`<br>`capacity`<br>`cephfs`<br>`cinder`<br>`claimRef`<br>`csi`<br>`fc`<br>`flexVolume`<br>`flocker`<br>`gcePersistentDisk`<br>`glusterfs`<br>`hostPath`<br>`iscsi`<br>`local`<br>`mountOptions`<br>`nfs`<br>`nodeAffinity`<br>`persistentVolumeReclaimPolicy`<br>`photonPersistentDisk`<br>`portworxVolume`<br>`quobyte`<br>`rbd`<br>`scaleIO`<br>`storageClassName`<br>`storageos`<br>`volumeMode`<br>`vsphereVolume`
`role` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Rule.v1**](doc/api/objects_role.md)<br>`rules` |  [**role-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#role-v1-rbac-authorization-k8s-io)
`rolebinding` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**rolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#rolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects`
`serviceaccount` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**serviceaccount-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#serviceaccount-v1-core)<br>`automountServiceAccountToken`<br>`imagePullSecrets`<br>`secrets`
`resourcequota` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**resourcequotaspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#resourcequotaspec-v1-core)<br>`hard`<br>`scopeSelector`<br>`scopes`
`networkpolicy` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**networkpolicyspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#networkpolicyspec-v1-networking-k8s-io)<br>`egress`<br>`ingress`<br>`podSelector`<br>`policyTypes`
**[Gateway APIs](https://gateway-api.sigs.k8s.io/reference/spec/#api-specification)**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`backendlbpolicy` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.BackendLBPolicy.v1alpha2**](doc/api/objects_gateway_api.md)<br>`targetRefs` |  [**backendlbpolicyspec-v1alpha2-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.BackendLBPolicySpec)<br>`sessionPersistence`
`backendtlspolicy` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.BackendTLSPolicy.v1alpha3**](doc/api/objects_gateway_api.md)<br>`targetRefs` |  [**backendtlspolicyspec-v1alpha3-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha3.BackendTLSPolicySpec)<br>`options`<br>`validation`
`gatewayclass` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**gatewayclassspec-v1-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewayClassSpec)<br>`controllerName`<br>`description`<br>`parametersRef`
`gateway` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Gateway.v1**](doc/api/objects_gateway_api.md)<br>`addresses`<br>`listeners` |  [**gatewayspec-v1-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewaySpec)<br>`backendTLS`<br>`gatewayClassName`<br>`infrastructure`
`grpcroute` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.GRPCRoute.v1**](doc/api/objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules`
`httproute` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.HTTPRoute.v1**](doc/api/objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules`
`referencegrant` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.ReferenceGrant.v1beta1**](doc/api/objects_gateway_api.md)<br>`from`<br>`to`
`tcproute` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.TCPRoute.v1alpha2**](doc/api/objects_gateway_api.md)<br>`parentRefs`<br>`rules`
`tlsroute` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.TLSRoute.v1alpha2**](doc/api/objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules`
`udproute` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.UDPRoute.v1alpha2**](doc/api/objects_gateway_api.md)<br>`parentRefs`<br>`rules`

**Other APIs**
HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`servicemonitor` | [**hull.ObjectBase.v1**](doc/api/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ServiceMonitor CRD**](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/crds/crd-servicemonitors.yaml)<br>`spec`

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

To render this analogously using the HULL library your chart needs to be [setup for using HULL](doc/setup.md). In the following section we assume the parent Helm chart is named `hull-test` and we use the `helm template` command to test render the `values.yaml`'s.

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

Read the additional documentation in the [documentation folder](./doc) on how to utilize the features of the HULL library to the full effect.
