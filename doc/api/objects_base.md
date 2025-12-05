# Base properties for all objects

The following configuration properties are available to all objects specified via HULL.

## JSON Schema Elements

### The `hull.ObjectBase.v1` properties

You can add the following optional properties to any object specified via HULL: 

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
`staticName` | A boolean switch. If set to true the object does not get a dynamically created name (see above) assigned but a name that only consists of the key name. Using static names is helpful in case you need to address the object from another Kubernetes object that is not part of the Helm chart and hence you want to refer to particular object in the cluster by a fixed name. Note that by setting `hull.config.general.noObjectNamePrefixes` to `true`, the individual `staticName` settings have no effect anymore | `false` | `true`<br>`false`
`metadataNameOverride` | A string field which overwrites the object instances component part in `metadata.name` and provides the full value of `metadata.labels.app.kubernetes.io/component`. While normally it is appropriate and convenient to derive the object instance names from the instance key in the object types dictionary, there may be special cases where having the possibility to alter the `metadata.name` of a defined object instance at deployment time is helpful.
`namespaceOverride` | A string field which, if set to a value that is not empty, overwrites the object instances `namespace`. CAUTION: Use with care since this _may_ not be supported Helm behavior to create objects in multiple namespaces within a single chart.
`enabled` | Needs to resolve to a boolean switch, it can be a boolean input directly or a transformation that resolves to a boolean value. If resolved to true or missing, the object will be rendered for deployment. If resolved to false, it will be omitted. This way you can predefine objects which are only enabled and created in the cluster in certain environments when needed. | `true` | `true`<br>`false`<br><br>`"_HULL_TRANSFORMATION_<<<NAME=hull.util.transformation.tpl>>><<<CONTENT=`<br>&#160;&#160;`{{`&#160;`(index`&#160;`.`&#160;`\"PARENT\").Values.hull.config.specific.enable_addon`&#160;`}}>>>"`
`annotations` | Dictionary with annotations to add to the Kubernetes objects main `metadata.annotations` section. The annotation value must be of string type on the Kubernetes side, but it is allowed to have boolean, integer or float type input on the HULL side. Any value will be automatically converted to string on rendering. | `{}` | `appImportance:`&#160;`"very`&#160;`low"`<br>`appStatus:`&#160;`"good"`
`labels` | Dictionary with labels to add to the Kubernetes objects main `metadata.labels` section. The label value must be of string type on the Kubernetes side, but it is allowed to have boolean, integer or float type input on the HULL side. Any value will be automatically converted to string on rendering. | | `label-1:`&#160;`DB_TYPE`<br>`label-2:`&#160;`"false"`<br>`label-3:`&#160;`false`<br>`label-4:`&#160;`true`<br>`label-5:`&#160;`"123"`<br>`label-6:`&#160;`123`<br>`label-7:`&#160;`"3.14"`<br>`label-8:`&#160;`3.14` | 
`sources` | A list of object instance keys from which default data will be loaded in the defined order. If key is not specified, default values will be loaded from _HULL_OBJECT_TYPE_DEFAULT_ instance only. | | `-`&#160;`default-instance-envs`<br> `-`&#160;`default-company-labels`


---
Back to [README.md](./../README.md)
