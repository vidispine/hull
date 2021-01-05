# Creating Custom Resources

Custom resource objects can be specified freely via HULL. This basically means you can create any custom resources of any CRDs. 

Only for this object type you need to explicitly provide the `kind` and `apiVersion` of the object. The `spec` part has no constraints.

## JSON Schema Elements

### The `hull.CustomResource.v1` options

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `apiVersion` | The API Version of the CR for which a matching CRD must exist in the system. | | `'master.mind.com/v1beta1'`
| `kind` | The API kind of the CR for which a matching CRD must exist in the system. | | `'Player'`
| `spec` | The free-form spec of the CR which must follow the strucure given in the matching CRD. | 