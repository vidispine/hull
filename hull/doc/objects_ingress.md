# Creating Ingresses

The HULL Ingress object offers some comfort features for specifying ingress objects.

## JSON Schema Elements

### The `hull.Ingress.v1` options

Properties can be set as they are defined in the [Kubernetes API's ingressspec spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#ingressspec-v1-networking-k8s-io). Only the below properties are interpreted by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `rules` | Dictionary with **`hull.Ingress.Rule.v1`** values to add to the ingresses `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Ingress.Rule.v1`** options of the ingress. See below for reference.  | `{}` |
| `tls` | Dictionary with **`hull.IngressTls.v1`** values to add to the ingresses `tls` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.IngressTls.v1`** options of the ingress. See below for reference.  | `{}` |

### The `hull.Ingress.Rule.v1` options

> The configuration of `hull.Ingress.Rule.v1` is based on a key value dictionary. 

Properties can be set as they are defined in the [Kubernetes API's ingressrule spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#ingressrule-v1-networking-k8s-io). Only the below properties are interpreted by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`http.paths` | Dictionary with **`hull.Ingress.Rule.Path.v1`** values to add to the `http.paths` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Ingress.Rule.Path.v1`** options of the container. See below for reference.  | `{}` |

### The `hull.Ingress.Rule.Path.v1` options

> The configuration of `hull.Ingress.Rule.Path.v1` is based on a key value dictionary. 

Properties can be set as they are defined in the [Kubernetes API's httpingresspath spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#httpingresspath-v1-networking-k8s-io). 

### The `hull.Ingress.Tls.v1` options

> The configuration of `hull.Ingress.Tls.v1` is based on a key value dictionary. 

Properties can be set as they are defined in the [Kubernetes API's ingresstls spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#ingresstls-v1-networking-k8s-io). Only the below properties are interpreted by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`staticName` | Specifies whether the `secretName` key of this `tls` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secretName` references a key defined in this helm chart. | `false` | `true`

## Examples