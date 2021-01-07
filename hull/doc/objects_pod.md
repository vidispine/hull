# Creating Pods 

Below sections detail the properties for creating pods via HULL.

## JSON Schema Elements

### The `hull.PodTemplate.v1` properties

For pod-based objects there is no need to create a `spec` property. The `spec.selector` property is automatically created under the hood to match the objects automatically created metadata. Any `spec.template.metadata` metadata is specified at top-level via `templateAnnotations` and `templateLabels` keys. 

So for all HULL based objects, the pod specific information is wrapped like this:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`templateAnnotations` | Dictionary with annotations to add to the Kubernetes objects `spec.template.metadata.annotations` section. | `{}` |  `appImportance:`&#160;`"low"`
`templateLabels` | Dictionary with labels to add to the Kubernetes objects `spec.template.metadata.labels` section. | `{}` | `appStatus:`&#160;`"bad"`
`pod`  | Specification of the inner pod in the form of **`hull.Pod.v1`**. See below for reference. | 

### The `hull.Pod.v1` properties

Properties can be set as they are defined in the [Kubernetes API's pod spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#podspec-v1-core).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`initContainers` | Dictionary with init containers to add to the pods `spec.initContainers` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Container.v1`** properties. See below for reference.  | `{}` |
`containers` | Dictionary with containers to add to the pods `spec.containers` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Container.v1`** properties. See below for reference. | `{}` || `{}` | 
`volumes` | Dictionary with volumes to add to the pods `spec.volumes` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Volume.v1`** properties. See below for reference. | `{}` |

### The `hull.Container.v1` properties

> The key-value pairs of value type `hull.Container.v1` are converted to an array on rendering

> The `name` property of the container is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's container spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#container-v1-core). 

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

Properties can be set as they are defined in the [Kubernetes API's envvar spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#envvar-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `valueFrom.configMapKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.configMapKeyRef` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.configMapKeyRef` references a key defined in this helm chart. | `false` | `true`
| `valueFrom.secretKeyRef.staticName` | Specifies whether the `name` key of this `valueFrom.secretKeyRef` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `valueFrom.secretKeyRef` references a key defined in this helm chart. | `false` | `true`

### The `hull.EnvFrom.v1` properties

> The key-value pairs of value type `hull.EnvFrom.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's envfromsource spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#envfromsource-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `configMapRef.staticName` | Specifies whether the `name` key of this `configMapRef` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `configMapRef` references a key defined in this helm chart. | `false` | `true`
| `secretRef.staticName` | Specifies whether the `name` key of this `secretRef` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secretRef` references a key defined in this helm chart. | `false` | `true`

### The `hull.ContainerPort.v1` properties

> The key-value pairs of value type `hull.ContainerPort.v1` are converted to an array on rendering

> The `name` property of the container's port is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's containerport spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#containerport-v1-core). 

### The `hull.VolumeMount.v1` properties

> The key-value pairs of value type `hull.VolumeMount.v1` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's volumemount spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#volumemount-v1-core). 

### The `hull.Volume.v1` properties

> The key-value pairs of value type `hull.Volume.v1` are converted to an array on rendering

> The `name` property of the volume is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's volume spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#volume-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `configMap.staticName` | Specifies whether the `name` key of this `configMap` refers to a fixed name of a ConfigMap in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `configMap` references a key defined in this helm chart. | `false` | `true`
| `persistentVolumeClaim.staticName` | Specifies whether the `name` key of this `persistentVolumeClaim` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `persistentVolumeClaim` references a key defined in this helm chart. | `false` | `true`
| `secret.staticName` | Specifies whether the `name` key of this `secret` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secret` references a key defined in this helm chart. | `false` | `true`

## Examples