# HULL: Helm UtiLity Library

## Introduction

This Helm library chart is designed to ease building, maintaining and configuring [Helm](https://helm.sh) charts. It can be added to any existing Helm chart and used without the risk of breaking existing Helm charts functionalities, see [adding HULL to a Helm chart](./doc/setup.md) for more information.

At the core, the HULL library chart provides Go Templating functions to create/render Kubernetes objects as YAML. But with the HULL library's functions no template files in the `/templates` folder need to be created, adapted and maintained to define the Kubernetes objects. Only an object definition in the `values.yaml`'s `hull` subchart key is required. JSON schema validation with the `values.schema.json` helps in directly producing Kubernetes API conforming objects for deployment.

The HULL library chart idea is partly inspired by the [common](
https://github.com/helm/charts/tree/master/incubator/common) Helm chart concept and for testing 

[![Gauge Badge](https://gauge.org/Gauge_Badge.svg)](https://gauge.org) .

## Feature Overview

As highlighted above, when included in a Helm chart the HULL library chart can take over the job of dynamically rendering Kubernetes objects from their given specifications from the `values.yaml` file alone. With YAML object construction deferred to the HULL library's Go Templating functions instead of custom YAML templates in the `/templates` folder you can centrally enforce best practices:

- Concentrate on what is needed to specify Kubernetes objects without having to add indidual YAML templates to your chart. This removes a common source of errors and maintanance from the regular Helm workflow. That the rendered output conforms to the Kubernetes API specification is validated by a large amount of CI unit tests. For more details refer to the documentation on [JSON Schema Validation](./doc/json_schema_validation.md).

- The single interface of the HULL library is used to both create and configure objects in charts for deployment. This fosters the mutual understanding of chart creators/maintainers and consumers of how the chart actually works and what it contains. To avoid any misconfiguration, the interface to the library being part of the `values.yaml` is JSON validated on input when using a IDE supporting this (e.g. VSCode) and also on rendering using the Helm integrated JSON Schema validation. For more details refer to the documentation on [JSON Schema Validation](./doc/json_schema_validation.md).

- Uniform and rich metadata is automatically attached to all objects created by the HULL library. 
  - Kubernetes standard labels as defined in https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/ are added to all objects metadata automatically. 
  - Within a Helm chart including HULL, further custom metadata can be set for 
    - all created K8S objects or 
    - all objects of a given K8S type or 
    - individual K8S objects. 

  For more details refer to the documentation on [Metadata](./doc/metadata.md).

- For all Kubernetes object types supported by HULL, all Kubernetes object properties are made available for configuration via the Helm charts `values.yaml`. Only updating the HULL chart to a newer Kubernetes API version is required to enable configuration of newer properties added to Kubernetes objects. This way continually patching existing Helm charts to support configuration of additional Kubernetes features is not required. The HULL charts are versioned to reflect the minimal Kubernetes API versions supported. 

- Enable automatic hashing of referenced configmaps and secrets to facilitate pod restarts on changes of configuration (work in progress)

- Flexible handling of ConfigMap and Secret input by choosing between inline specification of contents in `values.yaml` or import from external files for contents of larger sizes. When importing data from files the data can be either run through the templating engine or imported untemplated 'as is' if it already contains templating expressions that shall be passed on to the consuming application. For more details refer to the documentation on [ConfigMaps and Secrets](./doc/configmaps_secrets.md).

To learn more about the general architecture of the HULL library a see the [Architecture Overview](./doc/architecture.md)

**_IMPORTANT_**: 

> While there may be several benefits to rendering YAML via the HULL library please take note that it is a non-breaking addition to your Helm charts. The regular Helm workflow involving rendering of YAML templates in the `/templates` folder is completely unaffected by integration of the HULL library chart. Sometimes you might have very specific requirements on your configuration or object specification which the HULL library does not meet so you can use the regular Helm worflow for them and the HULL library for your more standard needs - easily in parallel in the same Helm chart. 

## Example

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

To render this analoguously using the HULL library the HULL library chart needs to be [setup for use](./doc/setup.md):

- Create an "nginx" helm chart that should contain the nginx deployment. The templates folder can remain empty for now.
- Inlude the HULL library chart as a subchart
- Copy the `hull_init.yaml` from the HULL charts root folder to the `/templates` folder of your parent chart. This is the only manual step that needs to be taken in order to use the HULL library chart.

Now to render the nginx deployment example with minimal effort you need to create the following `values.yaml` file in your parent chart:

```yaml
hull:  
  objects:
    deployment:
      nginx: # specify the nginx deployment under key 'nginx'
        replicas: 3
        pod:
          containers:
            image:
              repository: nginx
              tag: 1.14.2
```

This produces the following rendered deployment when running the `helm template` command:

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
```
This is a deployment with standard metadata auto-created and a service account associated with the deployment specified by only a few lines of YAML in the `values.yaml`.


## Testing and installing a chart

To test or install a chart the standard Helm v3 tooling is usable. See also the Helm documentation at the [Helm website](https://helm.sh). 

### Test a chart:

To inspect the outcome of a specific `values.yaml` configuration you can render the templates which would be deployed to Kubernetes and inspect them with the below command adapted to your needs:

  `<PATH_TO_HELM_V3_BINARY> template --debug --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> --output-dir <PATH_TO_OUTPUT_DIRECTORY> <PATH_TO_CHART_DIRECTORY>`

### Install or upgrade a release: 

Installing or upgrading a chart using HULL follows the standard procedures for every Helm chart:

  `<PATH_TO_HELM_V3_BINARY> upgrade --install --debug --create-namespace --atomic --namespace <CHART_RELEASE_NAMESPACE> --kubeconfig <PATH_TO_K8S_CLUSTER_KUBECONFIG> -f <PATH_TO_SYSTEM_SPECIFIC_VALUES_YAML> <RELEASE_NAME> <PATH_TO_CHART_DIRECTORY>`

## Creating and configuring chart

The tasks of creating and configuring a HULL based helm chart can be considered as two sides of the same coin. Both sides interact with the same interface (the HULL library) to specify the objects that should be created. The task from a creators/maintainers perspective is foremeost to provide the ground structure for the objects that make up the particular application which is to be wrapped in a helm chart. The consumer of the chart is tasked with appropriately adding his system specific context to the ground structure wherein he has the freedom to change and even add objects as needed to achieve his goals. At deploy time the creators base structure is merged with the consumers system-specific yaml file to build the complete configuration. Interacting via the same library interface fosters common understanding of how to work with the library on both sides and can eliminate most of the tedious copy&paste creation and examination heavy configuration processes.

So all that is needed to create a helm chart based on HULL is a standard scaffolded helm chart directory structure. Add the HULL library chart as a subchart, copy the `hull_init.yaml` from the HULL library chart to your parent Helm charts `/templates` folder. Then just configure the default objects to deploy via the `values.yaml` and you are done. There is no limit as to how many objects of whatever type you create for your products deployment.

But besides allowing to define complex objects and their relations with HULL you could also use it to wrap simple Kubernetes Objects you would otherwise either deploy via kubectl (being out of line from the management perspective with helm releases) or have to write a significant amnount of boilerplate to achieve this.

The base structure of the `values.yaml` understood by HULL is given here in the next section. This essentially forms the single interface for producing and consuming HULL based charts. Any object is only created in case it is defined and enabled in the `values.yaml`, this means you might want to preconfigure objects for consumers that would just need to enable them if they want to use them.

At the top level of the YAML structure, HULL distinguishes between `config` and `objects`. While the `config` subconfiguration is intended to deal with metadata and product specific settings, concrete objects to be rendered are specified under the `objects` key.

### _The `config` section_

Within the `config` section you can configure some general settings for your Helm chart.

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

### _The `objects` section_

The top-level object types beneath `hull.objects` represent the supported Kubernetes object types you might want to create instances from without creating custom templates in the `/templates` folder. Each object type is a dictionary where the entries values are the objects properties and each object has it's own key which is unique to the object type it belongs to. Further K8S object types can be added as needed to the library so it can easily be brought on par with a new Kubenetes release. 

#### _Keys of object instances_

One important aspect is that for all top-level object types, instances of a particular type are always identified by a key which is unique to the instance and object type combination. The same key can however be used for instances of different object types.

- do multi-layered merging of object properties by stacking `values.yaml` files on top of each other. You might start with defining the default object structure of the application or micro service defined in the given helm chart. Then you might add a `values.yaml` layer for a particular environment like staging or production. Then you might add a `values.yaml` layer for credentials. And so on. By uniquely identifying the instances of a particular K8s object type it becomes easy to adjust the objects properties through a multitude of layers.
- use the key of an instance is used for naming the instance. All instance names are constructed by the following ground rule: `{{ printf "%s-%s" .ReleaseName key }}`. This generates unique, dynamic names per object type and release + instance key combination. 

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

- each particular instance can have an `enabled` sub-field set to `true` or `false`. This way you can predefine instances of object types in your helm charts `values.yaml` but not deploy them in a default scenario. Or enable them by default and refrain from deploying them in a particular environment by disabling them in an overlayed system specific `values.yaml`. Note that unless you explicitly specify `enabled: false` each instance you define will be created by default, a missing `enabled` key is equivalent to `enabled: true`.

- cross-referencing objects within a helm chart by the instance key is a useful feature of the HULL library. This is possible in these contexts:
  -  when a reference to a ConfigMap or Secret comes into play you can just use the key of the targeted instance and the dynamic name will be rendered in the output. This is possible for referencing 
    - a ConfigMap or Secret behind a Volume or 
    - a Secret behind an Ingress' TLS specification or
    - a ConfigMap or Secret behind an environment value added to a container spec.
  - when referencing Services in the backend of an ingress' host you can specify the key to reference the backend service.
  
  > Note that you can in these cases opt to refer to a static name instead too. Adding a property `staticName: true` to the dictionary with your reference will force the referenced objects name to exactly match the name you entered.

#### _Values of object instances_

The values of object instance keys reflects the Kubernetes objects to create for the chart. To specify these objects efficiently, the available properties for configuration can be split into three groups:

1. [HULL basic object configuration](doc/object_base.md) whose properties are available for all object types and instances.
2. Specialized properties for some object types. Below is a reference of which object type supports which special properties in addition to the basic object configuration. If 
3. Kubernetes object properties. For each object type it is possible to specify all relevant Kubernetes properties. In case a HULL property overwrites a identically named Kubernetes property the HULL property has precedence.

    Besides using added options which are usable for the HULL objects you have all the matching Kubernetes object specific properties at your disposal for configuration. 

    But some of the typical top-level Kubernetes object properties and fields don't require setting them with HULL based objects because they can be deducted automatically:
    - the `apiVersion` and `kind` are determined by the HULL object type and Kubernetes API version and don't require to be explicitly set (except for objects of type `customresource`).
    - the top-level `metadata` dictionary on objects is handled by HULL via the `annotations` and `labels` fields and the naming rules explained above. So the `metadata` field does not require configuration and is hence not configurable for any object. 

Some lower level structures are also converted from the Kubernetes API array form to a dictionary form or are modified to improve working with them. This also enables more sophisticated merging of layers since arrays don't merge well, they only can be overwritten completely. Overwriting arrays however can make it hard to forget about elements that are contained in the default form of the array (you would need to know that they exist in the first place). In short, for a layered configuration approach without an endless amount of elements in arrays or dictionaries the dictionary is preferable for representing data since it offers a much better merging support.

Here is an overview of which top level properties are available for which object type in HULL. The HULL properties are grouped by the respective HULL JSON schema group they belong to. A detailed description of these groups and their properties is found in the documentation of this helm chart and the respective linked documents.

HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties
------------------------------ | --------------------| ----------------------------------
`configmap` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](doc/objects_configmaps_secrets.md)<br>`data` |  [**configmap-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#configmap-v1-core)<br>`binaryData`<br>`immutable`
`secret` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](doc/objects_configmaps_secrets.md)<br>`data` |  [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#secret-v1-core)<br>`immutable`<br>`stringData`<br>`type` 
`registry` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Registry.v1**](doc/objects_registry.md)<br>`server`<br>`username`<br>`password` | [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#secret-v1-core)
`deployment` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#deploymentspec-v1-apps)<br>`minReadySeconds`<br>`paused`<br>`progressDeadlineSeconds`<br>`replicas`<br>`revisionHistoryLimit`<br>`strategy` 
`job` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**jobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#jobspec-v1-batch)<br>`activeDeadlineSeconds`<br>`backoffLimit`<br>`completions`<br>`manualSelector`<br>`parallelism`<br>`ttlSecondsAfterFinished` 
`daemonset` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**daemonsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#daemonsetspec-v1-apps)<br>`minReadySeconds`<br>`revisionHistoryLimit`<br>`updateStrategy` 
`statefulset` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](doc/objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**statefulsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#statefulsetspec-v1-apps)<br>`podManagementPolicy`<br>`replicas`<br>`revisionHistoryLimit`<br>`updateStrategy`<br>`serviceName`<br>`volumeClaimTemplates` 
`cronjob` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Job.v1**](./README.md)<br>`job` | [**cronjobspec-v1beta1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#cronjobspec-v1beta1-batch)<br>`concurrencyPolicy`<br>`failedJobsHistoryLimit`<br>`schedule`<br>`startingDeadlineSeconds`<br>`successfulJobsHistoryLimit`<br>`suspend` 
`serviceaccount` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**serviceaccount-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#serviceaccount-v1-core)<br>`automountServiceAccountToken`<br>`imagePullSecrets`<br>`secrets`
`role` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**role-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#role-v1-rbac-authorization-k8s-io)<br>`rules`
`rolebinding` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**rolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#rolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects`
`clusterrole` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**clusterrole-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#clusterrole-v1-rbac-authorization-k8s-io)<br>`aggregationRule`<br>`rules`
`clusterrolebinding` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**clusterrolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#clusterrolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects`
`storageclass` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**storageclass-v1-storage-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#storageclass-v1-storage-k8s-io)<br>`allowVolumeExpansion`<br>`allowedTopologies`<br>`mountOptions`<br>`parameters`<br>`provisioner`<br>`reclaimPolicy`<br>`volumeBindingMode`
`persistentvolume` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#persistentvolumespec-v1-core)<br>`accessModes`<br>`awsElasticBlockStore`<br>`azureDisk`<br>`azureFile`<br>`capacity`<br>`cephfs`<br>`cinder`<br>`claimRef`<br>`csi`<br>`fc`<br>`flexVolume`<br>`flocker`<br>`gcePersistentDisk`<br>`glusterfs`<br>`hostPath`<br>`iscsi`<br>`lcal`<br>`mountOptions`<br>`nfs`<br>`nodeAffinity`<br>`persistentVolumeReclaimPolicy`<br>`photonPersistentDisk`<br>`portworxVolume`<br>`quobyte`<br>`rbd`<br>`scaleIO`<br>`storageClassName`<br>`storageos`<br>`volumeMode`<br>`vsphereVolume`
`persistentvolumeclaim` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumeclaimspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#persistentvolumeclaimspec-v1-core)<br>`accessModes`<br>`dataSource`<br>`resources`<br>`selector`<br>`storageClassName`<br>`volumeMode`<br>`volumeName`
`service` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Service.v1**](doc/objects_service.md)<br>`ports` | [**servicespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#servicespec-v1-core)<br>`clusterIP`<br>`externalIPs`<br>`externalName`<br>`externalTrafficPolicy`<br>`healthCheckNodePort`<br>`ipFamily`<br>`loadBalancerIP`<br>`loadBalancerSourceRanges`<br>`publishNotReadyAddresses`<br>`selector`<br>`sessionAffinity`<br>`sessionAffinityConfig`<br>`topologyKeys`<br>`type`
`ingress` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Ingress.v1**](doc/objects_ingress.md)<br>`tls`<br>`rules` | [**ingressclass-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#ingressclass-v1-networking-k8s-io)<br>`backend`<br>`ingressClassName`
`customresource` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.CustomResource.v1**](doc/objects_customresource.md)<br>`apiVersion`<br>`kind`<br>`spec`
`servicemonitor` | [**hull.ObjectBase.v1**](doc/objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ServiceMonitor CRD**](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/crds/crd-servicemonitors.yaml)<br>`spec`