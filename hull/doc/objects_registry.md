# Creating Registry Secrets

Registry Secrets can be created by specifying the needed information and letting the library take care of the correct storage of the information including Base64 encoding.

## JSON Schema Elements

### The `hull.Registry.v1` options

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `server` | Docker Registry host address. | `""` | `myregistry.azurecr.io`
| `username` | Docker Registry username. | `""` | `the_user`
| `password` | Docker Registry password. | `""` | `the_pAsSwOrD`