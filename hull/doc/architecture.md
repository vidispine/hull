# Architecture

Before discussing the architecture behind HULL it is useful to take a look at the motivation that spurred the creation of it.

## Motivation

In the context of Kubernetes and Helm there are basically two groups of people that work with Helm charts:
- the chart creators/maintainers
- the chart users

Let us first take at the problems that might arise for both groups before taking a look at the HULL architecture to see how some problems can be remedied.

### The chart maintainers view

While there is much freedom given to the chart designers and maintainers in how to abstract the configuration of the packaged applications, Helm unfortunately offers no fast, easy and maintenance free way to handle recurring demands. It is fully focussed on having custom YAML templates for all objects in a chart in order to produce output. But considering that Helm chart maintainers might create and have to maintain a large number of Helm charts this way of working can become difficult. 

First of, getting started on building helm charts is challenging - especially for someone not experienced with the concepts of Kubernetes, Helm, YAML and Go Templating and all the relations between them which are needed to create sound helm charts. Furthermore, YAML and string templating don't play nice together which is something [rightfully criticized](https://grafana.com/blog/2020/01/09/introducing-tanka-our-way-of-deploying-to-kubernetes/). It can become very finicky to produce valid YAML output with templating expressions. Typically starting a new helm chart from scratch requires a significant amount of copying and pasting templates from existing charts and adapting them to the new products needs. This is a time consuming and error prone process. 
 
Once charts have been created and published they need to be maintained. A maintainer maintaining a single Helm chart can reasonably do his work but let us assume it is required of her/him to maintain many helm charts. Then the amount of (for the large part) duplicated YAML blocks in templates grows very fast. Assuming you need to fix a conceptional issue you likely need to do this in a variety of files each time which is tedious and time consuming.

### The chart users view

Initially, chart users are faced with the same steep learning curve as the maintainers. They also need to be familiar with the underlying concepts to create a proper deployment configuration. This is worsened by the fact that each helm chart is basically a unique artifact with it's unique underlying implications of how it should be configured. 

But any more advanced user of Helm will be aware of the objects as they are represented by the Kubernetes API. In order to specify the objects with the properties they have in mind they need to understand the individual chart creators assumptions on how to configure the chart and the relations behind. As an analogy, it is comparable to someone who wants to speak english (Kubernetes YAML) being told he has to learn portuguese (Helm YAML) and all regional portuguese dialects (individual Helm chart interfaces) to do so.

The best practices guidelines that are available do cover some ground to align chart writing and foster common understanding but still leave most design aspects to the maintainers. From personal experience it is almost always needed to inspect the files in the `/templates` folder to learn about the effects of changing configuration parameters in the `values.yaml`. 

Moreover, depending on the requirements and preferences of the chart maintainer it is often the case that features required for a particular user are not implemented in the chart at all. To give an example of this, let's take a look at specifying `imagePullSecrets` for deployments within a helm chart:
- It might not be possible to specify them with the given chart in case the chart maintainers did not opt for implementing them, maybe being focused on public cloud deployments only. In this case you need to submit a pull request, modify locally, fork or something else to fulfill your requirement.
- The helm chart might have very different expectations on how they should be specified. Looking at some public helm charts available:
  - The `cerebro` helm chart at `https://github.com/helm/charts/blob/master/stable/cerebro/templates/deployment.yaml` requires you to specify `imagePullSecrets` as an array/list of values (excluding the `name` keys) per image:
  
    ```yaml
    {{- if .Values.image.pullSecrets }}
    imagePullSecrets:
    {{- range .Values.image.pullSecrets }}
    - name: {{ . }}
    {{- end }}
    {{- end }}
    ```
  - The `sonarqube` helm chart at `https://github.com/helm/charts/blob/master/stable/cerebro/templates/deployment.yaml` requires you to specify `imagePullSecrets` as a string. This means you can only specify one:
  
    ```yaml
    {{- if .Values.image.pullSecret }}
    imagePullSecrets:
    - name: {{ .Values.image.pullSecret }}
    {{- end }}
    ```

  - The `prometheus` helm chart at `https://github.com/helm/charts/blob/master/stable/prometheus/templates/deployments/alertmanager.yaml` however wants `imagePullSecrets` provided as an array of key-value pairs with repeated `name` keys:
  
    ```yaml
    {{- if .Values.imagePullSecrets }}
    imagePullSecrets:
    {{ toYaml .Values.imagePullSecrets | indent 2 }}
    {{- end }}
    ```

This is not helpful to the user to have an intuition of what he needs to do. The HULL library can step in to solve these issues to a large degree.

### Conclusion

There are various groups of people that work with Helm. There might be a group of people concerned with maintaining and installing a single specific chart to the best of their effort. In this case the regular Helm workflow might be suited for them well enough.

But there are also people who maintain and/or consume a larger number of charts which likely are overwhelmed by the various individual design approaches to creating Helm charts. To this group, using the HULL library can omit the tedious YAML template creation and placeholder logic by offering a common interface to specifying objects directly, allowing the consumer to specify complete Kubernetes objects out-of-the-box and support frequent use-cases by a light abstraction layer.

## Components

At the core of the HULL library is the interplay between `values.yaml`, [`values.schema.json`](./../values.schema.json), [`hull.yaml`](./../hull.yaml) and the template files in [`/templates`](./../templates) that come with HULL.

### The parent charts `values.yaml`

For the HULL related functionalities only entries under the `hull` sub-key are relevant. No other top level key is relevant for HULL so it can co-exist with any other Helm chart configuration properties.

### The [`values.schema.json`](./../values.schema.json)

The `values.schema.json` of each HULL library release is built from the respective version of the Kubernetes API JSON Schema which is:
- extended with the HULL specific properties to provide the HULL specific functionalities and
- minor modifications to the strict K8S JSON schema to allow co-existence with the HULL specific properties.

This means that misconfigurations of the `values.yaml` `hull` subsection are either visible on input directly or catched on rendering the objects.

### The [`hull.yaml`](./../hull.yaml)

The `hull.yaml` needs to be placed in the parents charts `/templates` folder. It contains a loop over all handled object types and their specific configurational properties. Within the loop all objects of the handled object types (as specified in `values.yaml`) are iterated over and the corresponding rendering function is called for the specified and enabled object. 

### The [`/templates`](./../templates)

The templates folder in HULL contains only functions as it is mandatory for Helm library charts. 

## End-to-End process

The end to end process using HULL contains the following phases:

1. [Setup of Helm chart using HULL](setup.md).
2. Define the input to the Helm chart in `values.yaml` and maybe additional `values.yaml`'s which are superimposed. This can be heavily supported by [IDE`s that offer live input validation via JSON schema](json_schema_validation.md).
3. If you are satisfied with the specification of objects you can test render your chart to check the result or install it in a test cluster. Behind the scenes the following takes place:
    
    1. JSON Schema validation of merged `values.yaml` via the `values.schema.json` included in HULL. It is based on the strict Kubernetes API schema and modified to incorporate the schemas of the additional HULL objects.

        ⚠️ **Any schema violations will prevent further processing.** ⚠️

    2. The `hull.yaml` in the templates folder is processed. 
  
        First the complete `values.yaml` dictionary is traversed and any [transformations](./transformations.md) provided are evaluated. This includes all objects including `_HULL_OBJECT_TYPE_DEFAULT_` instances and `sources` which are not rendered themselves.
    
        Next an iteration over all implemented object types and defined and enabled object instances hands over to the object instance definition to the appropriate rendering template. Different basic rendering templates are triggered for:

        - objects with a simple structure:
          - `serviceaccount`
          - `storageclass`
          - `customresource`
          - `priorityclass`
          - `endpoints`
        - objects with a simple structure depending on RBAC enablement:
          - `rolebinding`
          - `clusterrolebinding`
        - objects with a role based structure depending on RBAC enablement:
          - `role`
          - `clusterrole`
        - objects with a `spec` field:
          - `perstistentvolume`
          - `persistentvolumeclaim`
          - `servicemonitor`
          - `poddisruptionbudget`
          - `resourcequota`
          - `networkpolicy`
          - `ingressclass`
        - objects which are based on pod definitions
          - `deployment`
          - `job`
          - `daemonset`
          - `statefulset`
        - objects which are based on webhook definitions
          - `mutatingwebhookconfiguration`
          - `validatingwebhookconfiguration`
        - objects with individual templates:
          - `configmap`
          - `secret`
          - `registry`
          - `service`
          - `ingress`
          - `cronjob`
          - `horizontalpodautoscaler`

        Then each object is processed individually:
        
        1. Apply object type defaults from the `_HULL_OBJECT_TYPE_DEFAULT_` instances and merge referenced `sources` into the object source specification. 
        2. Create the [metadata section](metadata.md) of the object
        3. Process all properties handled by HULL
        4. Add remaining Kubernetes API schema properties that were defined

    3. The output is all defined objects concatenated in one file with `template` command or handed over to the Kubernetes cluster API for deployment with `install` command.
---
Back to [README.md](./../README.md)