# Creating Roles

The HULL Roles allow to have key value pair `rules` to define the rules. 

⚠️ **For downwards compatibility it is alternatively still possible to specify the `rules` as an array, however no mixed-style of arrays and key value pairs is possible!** ⚠️

## JSON Schema Elements

### The `hull.Role.v1` properties

Properties can be set as they are defined in the [Kubernetes API's roles spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#role-v1-rbac-authorization-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `rules` | Dictionary with PolicyRules to add to the ClusterRole's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.PolicyRules.v1`** properties. See below for reference. | `{}` || `{}` 


### The `hull.ClusterRole.v1` properties

Properties can be set as they are defined in the [Kubernetes API's clusterroles spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#clusterrole-v1-rbac-authorization-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `rules` | Dictionary with PolicyRules to add to the ClusterRole's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The **`hull.PolicyRules.v1`** properties. See below for reference. | `{}` || `{}` 

### The `hull.PolicyRules.v1` properties

> The key-value pairs of value type `hull.PolicyRules.v1` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's policyrules spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#policyrule-v1-rbac-authorization-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the key-value-pair will be rendered for deployment. If resolved to false, it will be omitted from rendering. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` |

---
Back to [README.md](./../README.md)