# Creating Services

The HULL Service object is a thin wrapper around the Kubernetes Service providing the possibility to specify the `ports` via keys.

## JSON Schema Elements

### The `hull.Service.v1` properties

Properties can be set as they are defined in the [Kubernetes API's service spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#service-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `ports` | Dictionary with **`hull.ServicePort.v1`** values to add to the containers `ports` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.ServicePort.v1`** properties of the container. See below for reference.  | `{}` |

### The `hull.ServicePort.v1` properties

> The key-value pairs of value type `hull.ServicePort.v1` are converted to an array on rendering

> The `name` property of the service's port is derived from the key.

Properties can be set as they are defined in the [Kubernetes API's serviceport spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#serviceport-v1-core). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` |  


---
Back to [README.md](./../README.md)
