# Creating Ingresses

The HULL Ingress object offers some comfort features for specifying ingress objects.

## JSON Schema Elements

### The `hull.Ingress.v1` properties

Properties can be set as they are defined in the [Kubernetes API's ingressspec spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.35/#ingressspec-v1-networking-k8s-io).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `rules` | Dictionary with **`hull.Ingress.Rule.v1`** values to add to the ingresses `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Ingress.Rule.v1`** properties of the ingress. See below for reference. | `{}` | |
| `tls` | Dictionary with **`hull.IngressTls.v1`** values to add to the ingresses `tls` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.IngressTls.v1`** properties of the ingress. See below for reference. | `{}` | |

### The `hull.Ingress.Rule.v1` properties

> The key-value pairs of value type `hull.Ingress.Rule.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's ingressrule spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.35/#ingressrule-v1-networking-k8s-io).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | `true`<br>`false`<br><br>`_HT?hull.config.specific.enable_addon` |
| `http.paths` | Dictionary with **`hull.Ingress.Rule.Path.v1`** values to add to the `http.paths` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.Ingress.Rule.Path.v1`** properties of the container. See below for reference. | `{}` | |

### The `hull.Ingress.Rule.Path.v1` properties

> The key-value pairs of value type `hull.Ingress.Rule.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's httpingresspath spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.35/#httpingresspath-v1-networking-k8s-io).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | |

### The `hull.Ingress.Tls.v1` properties

> The key-value pairs of value type `hull.Ingress.Tls.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's ingresstls spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.35/#ingresstls-v1-networking-k8s-io).

However the properties listed below are overwritten or added by HULL:

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | |
| `staticName` | Specifies whether the `secretName` key of this `tls` refers to a fixed name of a Secret in the cluster or not. <br>If the field does not exist or is set to `false`, the `name` field of this `secretName` references a key defined in this helm chart. | `false` | `true` |

---
Back to [README.md](/README.md)
