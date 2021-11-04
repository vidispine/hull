# Creating Roles

The HULL Roles allow to have key value pair `rules` to define the rules. 

⚠️ **For downwards compatibility it is alternatively still possible to specify the `rules` as an array, however no mixed-style of arrays and key value pairs is possible!** ⚠️

## JSON Schema Elements

### The `hull.Role.v1` properties

Properties can be set as they are defined in the [Kubernetes API's roles spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#role-v1-rbac-authorization-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `rules` | Dictionary with [**`io.k8s.api.rbac.v1.PolicyRule`**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#policyrule-v1-rbac-authorization-k8s-io) values to add to the roles `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`io.k8s.api.rbac.v1.PolicyRule`**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#policyrule-v1-rbac-authorization-k8s-io) properties of the rule. | `{}` |

### The `hull.ClusterRole.v1` properties

Properties can be set as they are defined in the [Kubernetes API's clusterroles spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#clusterrole-v1-rbac-authorization-k8s-io). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `rules` | Dictionary with [**`io.k8s.api.rbac.v1.PolicyRule`**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#policyrule-v1-rbac-authorization-k8s-io) values to add to the roles `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`io.k8s.api.rbac.v1.PolicyRule`**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#policyrule-v1-rbac-authorization-k8s-io) properties of the rule. | `{}` |

---
Back to [README.md](./../README.md)