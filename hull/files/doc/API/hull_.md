# The `hull` root element

The tasks of creating and configuring a HULL based helm chart can be considered as two sides of the same coin. Both sides interact with the same interface (the HULL library) to specify the objects that should be created. The task from a creators/maintainers perspective is foremost to provide the ground structure for the objects that make up the particular application which is to be wrapped in a Helm chart. The consumer of the chart is tasked with appropriately adding his system specific context to the ground structure wherein he has the freedom to change and even add or delete objects as needed to achieve his goals. At deploy time the creators base structure is merged with the consumers system-specific yaml file to build the complete configuration. Interacting via the same library interface fosters common understanding of how to work with the library on both sides and can eliminate most of the tedious copy&paste creation and examination heavy configuration processes.

So all that is needed to create a helm chart based on HULL is a standard scaffolded helm chart directory structure. Add the HULL library chart as a sub-chart, copy the `hull.yaml` from the HULL library chart to your parent Helm charts `/templates` folder. Then just configure the default objects to deploy via the `values.yaml` and you are done. There is no limit as to how many objects of which type you create for your deployment package.

But besides allowing to define more complex applications with HULL you could also use it to wrap simple Kubernetes Objects you would otherwise either deploy via kubectl (being out-of-line from the management perspective with helm releases) or have to write a significant amount of Helm boilerplate templates to achieve this. 

The base structure of the `values.yaml` understood by HULL is given here in the next section. This essentially forms the single interface for producing and consuming HULL based charts. Any object is only created in case it is defined and enabled in the `values.yaml`, this means you might want to pre-configure objects for consumers that would just need to enable them if they want to use them.

At the top level of the YAML structure, HULL distinguishes between `config` and `objects`. While the `config` sub-configuration is intended to deal with chart specific settings such as metadata and product settings, the concrete Kubernetes objects to be rendered are specified under the `objects` key.
An additional third top level key named `version` is allowed as well, when this is being set to the HULL charts version for example during the parent Helm Charts release pipeline it will automatically populate the label `vidispine.hull/version`on all objects indicating the HULL version that was used to render the objects.

So the start defining your charts configuration and objects, create the following structure in the parent chart:

```
hull:
  config: # Chart configuration and shared resources go here
    ...
  objects: # Chart objects are created here
    ...
  version: # Optional field to hold the version of HULL
    ... 
```