# Creating Webhooks

The HULL Webhook objects allows to reference a chart internal webhook by simple key name.

## JSON Schema Elements

### The `hull.MutatingWebhook.v1` properties

Properties can be set as they are defined in the [Kubernetes API's mutatingwebhookconfiguration spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#mutatingwebhookconfiguration-v1-admissionregistration-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `webhooks` | Dictionary with **`hull.MutatingWebhook.Webhook.v1`** values to add to the containers `webhooks` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.MutatingWebhook.Webhook.v1`** properties of the container. See below for reference.  | `{}` |

### The `hull.MutatingWebhook.Webhook.v1` properties

> The key-value pairs of value type `hull.MutatingWebhook.Webhook.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's mutatingwebhook spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#mutatingwebhook-v1-admissionregistration-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | 

### The `hull.ValidatingWebhook.v1` properties

Properties can be set as they are defined in the [Kubernetes API's validatingwebhookconfiguration spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#validatingwebhookconfiguration-v1-admissionregistration-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `webhooks` | Dictionary with **`hull.ValidatingWebhook.Webhook.v1`** values to add to the containers `webhooks` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.ValidatingWebhook.Webhook.v1`** properties of the container. See below for reference.  | `{}` |

### The `hull.ValidatingWebhook.Webhook.v1` properties

> The key-value pairs of value type `hull.ValidatingWebhook.Webhook.v1` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's validatingwebhook spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#validatingwebhook-v1-admissionregistration-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | 

---
Back to [README.md](./../README.md)