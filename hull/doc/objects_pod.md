# Creating Pods 

Below sections detail the properties for creating pods via HULL.

## JSON Schema Elements

### The `hull.PodTemplate.v1` properties

For pod-based objects there is no need to create a `spec` property. The `spec.selector` property is automatically created under the hood to match the objects automatically created metadata. Any `spec.template.metadata` metadata is specified at top-level via `templateAnnotations` and `templateLabels` keys. 

⚠️The `selector` property of pod-based objects will be automatically populated to match the exact combination of the auto-generated `hull.config.general.metadata.labels.common` fields `app.kubernetes.io/name`, `app.kubernetes.io/instance` and `app.kubernetes.io/component`. An exception is made for the objects of type `job` where no `selector` field is set because Kubernetes jobs deal with the `selector` implicitly. If need be it is possible to set `selector` manually for the particular `job` however.⚠️

So for all HULL based objects, the pod specific information is wrapped like this:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`templateAnnotations` | Dictionary with annotations to add to the Kubernetes objects `spec.template.metadata.annotations` section. | `{}` |  `appImportance:`&#160;`"low"`
`templateLabels` | Dictionary with labels to add to the Kubernetes objects `spec.template.metadata.labels` section. | `{}` | `appStatus:`&#160;`"bad"`
`pod`  | Specification of the inner pod in the form of **`hull.Pod.v1`**. See below for reference. | 

### The `hull.Pod.v1` properties

Properties can be set as they are defined in the [Kubernetes API's pod spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#podspec-v1-core).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`initContainers` | Dictionary with init containers to add to the pods `spec.initContainers` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Container.v1`** properties. See below for reference.<br><br>⚠️ **Due to the conversion between dictionary and array the order of elements is changed so that all keys are alphanumerically sorted ascending before the key-value pairs are converted to array elements. Unfortunately this cannot be avoided. In the case of initContainers - where order of items is important for order of execution - this means that the initContainer keys need to be chosen so that their alphanumeric order matches the desired order of execution. This can be simply achieved by eg. adding prefixes `01_`, `02_`, ... to the initContainer key names.** ⚠️ | `{}` |
`containers` | Dictionary with containers to add to the pods `spec.containers` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Container.v1`** properties. See below for reference. | `{}` || `{}` | 
`volumes` | Dictionary with volumes to add to the pods `spec.volumes` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Volume.v1`** properties. See below for reference. | `{}` |

### The `hull.Container.v1` properties

> The key-value pairs of value type `hull.Container.v1` are converted to an array on rendering

> The `name` property of the container is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's container spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#container-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`image`  | Specification of the image in form of **`hull.Image.v1`**. See below for reference. | 
`env` | Dictionary with **`hull.Env.v1`** values to add to the containers `env` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Env.v1`** properties of the container. See below for reference.  | `{}` |
`envFrom` | Dictionary with **`hull.EnvFrom.v1`** values to add to the containers `envFrom` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.EnvFrom.v1`** properties of the container. See below for reference.  | `{}` |
`ports` | Dictionary with **`hull.ContainerPort.v1`** values to add to the containers `ports` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Port.v1`** properties of the container. See below for reference.  | `{}` |
`volumeMount` | Dictionary with **`hull.VolumeMount.v1`** values to add to the containers `volumeMounts` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.VolumeMount.v1`** properties of the container. See below for reference.  | `{}` |

### The `hull.Image.v1` properties

Definition of container images is split into multiple parts to allow better support of switching the registry endpoints throughout the whole chart.

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `registry` | Optional endpoint of the repository. If set will produce a prefix and appended `/`. | ` ` | `myregistry.azure.cr`
| `repository` | Name/Repository of the container image | | `apps/videoeditor`
| `tag` | Tag of the container image | | `20.1.3-pre.321`

### The `hull.Env.v1` properties

> The key-value pairs of value type `hull.Env.v1` are converted to an array on rendering

> The `name` property of the environment variable is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's envvar spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#envvar-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` |
| `valueFrom.configMapKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.configMapKeyRef` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.configMapKeyRef` references a key defined in this helm chart. | `false` | `true`
| `valueFrom.configMapKeyRef.hashsumAnnotation` | If present and true, the contents of the referenced ConfigMap data key is automatically hashed and added as an annotation to the pod template metadata annotations (`templateAnnotations`). <br><br>If set to true, any change to the referenced content will trigger a pod restart on upgrade. | `false` | `true`
| `valueFrom.secretKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.secretKeyRef` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.secretKeyRef` references a key defined in this helm chart. | `false` | `true`
| `valueFrom.secretKeyRef.hashsumAnnotation` | If present and true, the contents of the referenced Secret data key is automatically hashed and added as an annotation to the pod template metadata annotations (`templateAnnotations`). <br><br>If set to true, any change to the referenced content will trigger a pod restart on upgrade. | `false` | `true`

### The `hull.EnvFrom.v1` properties

> The key-value pairs of value type `hull.EnvFrom.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's envfromsource spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#envfromsource-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | 
| `configMapRef.staticName` | Specifies whether the `name` key of this `configMapRef` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `configMapRef` references a key defined in this helm chart. | `false` | `true`
| `valueFrom.configMapRef.hashsumAnnotation` | If present and true, the contents of the referenced ConfigMap data keys are automatically hashed and added as annotations to the pod template metadata annotations (`templateAnnotations`). <br><br>If set to true, any change to the referenced content will trigger a pod restart on upgrade. | `false` | `true`
| `secretRef.staticName` | Specifies whether the `name` key of this `secretRef` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secretRef` references a key defined in this helm chart. | `false` | `true`
| `valueFrom.secretRef.hashsumAnnotation` | If present and true, the contents of the referenced Secret data keys are automatically hashed and added as annotations to the pod template metadata annotations (`templateAnnotations`). <br><br>If set to true, any change to the referenced content will trigger a pod restart on upgrade. | `false` | `true`

### The `hull.ContainerPort.v1` properties

> The key-value pairs of value type `hull.ContainerPort.v1` are converted to an array on rendering

> The `name` property of the container's port is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's containerport spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#containerport-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` |  

### The `hull.VolumeMount.v1` properties

> The key-value pairs of value type `hull.VolumeMount.v1` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's volumemount spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#volumemount-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` |  
| `hashsumAnnotation` | If present and true, the setting takes effect when the volume for this mount is a ConfigMap or Secret reference. In case of a present `subPath` property, the ConfigMaps or Secrets data `subPath` key content is automatically hashed and added as annotations to the pod template metadata annotations (`templateAnnotations`). In case of a missing `subPath`, all data keys contents of the ConfigMap or Secret are automatically hashed and added as annotations to the pod template metadata annotations (`templateAnnotations`). <br><br>If set to true, any change to the referenced content will trigger a pod restart on upgrade. | `false` | `true`

### The `hull.Volume.v1` properties

> The key-value pairs of value type `hull.Volume.v1` are converted to an array on rendering

> The `name` property of the volume is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's volume spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#volume-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | 
`active` | Using the `active` property it becomes possible to specify multiple different sources of volumes (such as `emptyDir`, `persistentVolumeClaim`, `secret` ...) for one `volume` entry and decide which one to actually render in the end. Kubernetes does not allow one `volume` entry to have specifications for multiple sources and will throw an error if it detects this. Sometimes however it is reasonable to start with an `emptyDir` for a particular `volume`'s default source and for some reason change it to some other persistent source for your actual environment. Setting `active` allows to neglect all other specified sources except the `active` one. <br><br>The value of `active` - if provided - must match an existing volume source key name and the exact volume source must be specified to select this volume source's definition for rendering. <br><br>If `active` property is not present<br> only one volume source definition is allowed to exist for the volume entry, otherwise Kubernetes API will not accept the `volume`.  | | `awsElasticBlockStore`<br>`azureDisk`<br>`azureFile`<br>`cephfs`<br>`cinder`<br>`configMap`<br>`csi`<br>`downwardAPI`<br>`emptyDir`<br>`ephemeral`<br>`fc`<br>`flexVolume`<br>`flocker`<br>`gcePersistentDisk`<br>`gitRepo`<br>`glusterfs`<br>`hostPath`<br>`iscsi`<br>`nfs`<br>`persistentVolumeClaim`<br>`photonPersistentDisk`<br>`portworxVolume`<br>`projected`<br>`quobyte`<br>`rbd`<br>`scaleIO`<br>`secret`<br>`storageos`<br>`vsphereVolume`
| `configMap.staticName` | Specifies whether the `name` key of this `configMap` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `configMap` references a key defined in this helm chart. | `false` | `true`
| `persistentVolumeClaim.staticName` | Specifies whether the `name` key of this `persistentVolumeClaim` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `persistentVolumeClaim` references a key defined in this helm chart. | `false` | `true`
| `secret.staticName` | Specifies whether the `name` key of this `secret` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secret` references a key defined in this helm chart. | `false` | `true`

---
Back to [README.md](./../README.md)

