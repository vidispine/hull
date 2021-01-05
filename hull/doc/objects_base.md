# Base options for all objects

The following configuration properties are available to all objects specified via HULL.

## JSON Schema Elements

### The `hull.ObjectBase.v1` options

You can add the following optional properties to any object specified via HULL: 

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`staticName` | A boolean switch. If set to true the object does not get a dynamically created name (see above) assigned but a name that only consists of the key name. Using static names is helpful in case you need to address the object from another Kubernetes object that is not part of the Helm chart and hence you want to refer to particular object in the cluster by a fixed name. | `false` | `true`<br>`false`
`enabled` | A boolean switch. If set to true or missing, the object will be rendered for deployment. If set to false, it will be omitted. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | `true`<br>`false`
`annotations` | Dictionary with annotations to add to the Kubernetes objects main `metadata.annotations` section | `{}` | `appImportance:`&#160;`"very`&#160;`low"`
`labels` | Dictionary with labels to add to the Kubernetes objects main `metadata.labels` section. | `{}` | `appStatus:`&#160;`"good"`

## Examples