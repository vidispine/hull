# Creating Services

The HULL Service object is a thin wrapper around the Kubernetes Service providing the possibility to specify the `ports` via keys.

## JSON Schema Elements

### The `hull.Service.v1` options

Properties can be set as they are defined in the [Kubernetes API's service spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#service-v1-core). Only the below properties are interpreted by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `ports` | Dictionary with **`hull.ServicePort.v1`** values to add to the containers `ports` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.ServicePort.v1`** options of the container. See below for reference.  | `{}` |

### The `hull.ServicePort.v1` options

> The configuration of `hull.ServicePort.v1` is based on a key value dictionary. 

> The key name here is the `name` property of the service port to set.

Properties can be set as they are defined in the [Kubernetes API's serviceport spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#serviceport-v1-core). 
