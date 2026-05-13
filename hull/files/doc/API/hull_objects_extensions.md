# Creating Objects from HULL API exensions

Some object types are exclusive to HULL and have no direct representation in the Kubernetes API. These extension API objects aim at extending HULLs usefulness.

## Creating Generic Objects

Generic objects can be specified freely via HULL. There are no constraints on the fields of the object besides the need to specify the `kind` and `apiVersion` of the object.

The purpose of Generic objects is to provide a way to specify custom objects that may be rarely needed and therefore don't have a full representation in the list of HULL objects. They are similar to the CustomResource objects below but don't have the requirement of a `spec` field to be present so they can be universally used.

### JSON Schema Elements

#### The `hull.Generic.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `apiVersion` | The API Version of the CR for which a matching CRD must exist in the system. | | `'master.mind.com/v1beta1'` |
| `kind` | The API kind of the CR for which a matching CRD must exist in the system. | | `'Player'` |

## Creating Custom Resources

Custom resource objects can be specified freely via HULL. This basically means you can create any custom resources of any CRDs. The difference between CustomResource objects and Generic objects is that the `spec` field must be present in the object specification.

For this object type you need to explicitly provide the `kind` and `apiVersion` of the object. The `spec` part has no constraints.

### JSON Schema Elements

#### The `hull.CustomResource.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `apiVersion` | The API Version of the CR for which a matching CRD must exist in the system. | | `'master.mind.com/v1beta1'` |
| `kind` | The API kind of the CR for which a matching CRD must exist in the system. | | `'Player'` |
| `spec` | The free-form spec of the CR which must follow the structure given in the matching CRD. | | |

## Creating Registry Secrets

Registry Secrets can be created by specifying only the needed information and letting the library take care of the correct storage of the information including Base64 encoding.

### JSON Schema Elements

#### The `hull.Registry.v1` properties

| Parameter | Description | Default | Example |
| --------- | ----------- | ------- | ------- |
| `server` | Docker Registry host address. | `""` | `myregistry.azurecr.io` |
| `username` | Docker Registry username. | `""` | `the_user` |
| `password` | Docker Registry password. | `""` | `the_pAsSwOrD` |

---
Back to [README.md](/README.md)
