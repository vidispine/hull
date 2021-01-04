# Architecture

## Motivation

Before looking at the actual architecture of the HULL library chart it is helpful to discuss the motivation of what drives it:

In the context of Kubernetes and Helm there are basically two groups of people that work with Helm charts:
- the chart maintainers
- the chart users

### The chart maintainers view

While there is much freedom given to the chart designers and maintainers in how to abstract the configuration of the packaged applications, Helm unfrotunately offers no fast, easy and maintanance free way to handle recurring demands. Generally it is focussed on having custom YAML templates per chart in order to produce output. But Helm chart maintainers might create and maintain a varying number of Helm charts. Let us take a look at aspects of creating Helm charts from a creators/maintainers point of view. 

Getting started on building helm charts is challenging, especially for someone not experienced with the concepts of Kubernetes, Helm, YAML and Go Templating and all the relations between them which are needed to create sound helm charts. Furthermore, YAML and string templating don't go well together which is something [rightfully critized](https://grafana.com/blog/2020/01/09/introducing-tanka-our-way-of-deploying-to-kubernetes/), it can become very finicky to produce valid YAML output with templating expressions. Typically starting a new helm chart from scratch requires a significant amount of copying and pasting templates from existing charts and adapting them to the new products needs. This is a time consuming and error prone process. 
 
Once charts have been created and published they need to be maintained. Maintaining a single Helm chart can be reasonable done manually but let us assume it is required to maintain many helm charts, then the amount of (for the most part) duplicated YAML blocks in templates grows very fast. Assuming you need to fix a conceptional issue you likely need to do this in a variety of files each time which is tedious and time consuming.

### The chart users view

Initially chart users are faced with the same steep learning curve as the maintainers. They also need to be familiar with the underlying concepts to create a proper deployment configuration. This is worsened by the fact that each helm chart is basically a unique artifact with it's unique underlying implications of how it should be configured. Any more advanced user of Helm will be aware of the objects as they are represented by the Kubernetes API. But in order to specify the object with the properties they have in mind they need to understand the individual charts assumptions and the Helm machinery in the back. As an analogy, it is comparable to someone who wants to speak english (Kubernetes) being told he has to learn portugese (Helm) and all regional portugese dialects (actual Helm chart interfaces) to do so.

The best practices guidelines that are available do cover some ground to align chart writing and understanding but still leave most design aspects to the maintainers. From personal experience you almost always need to inspect the files in the `/templates` folder to learn about the effects of changing configuration parameters in the `values.yaml`. 

Additionally, depending on the requirements and preferences of the chart maintainer it is often the case that features required for a particular user are not implemented in the chart at all. To give an example of this, let's take a look at specifying `imagePullSecrets` for deployments within a helm chart:
- It might not be possible to specify them with the given chart in case the chart maintainers did not opt for implementing them, maybe being focused on public cloud deployments only. In this case you need to submit a pull requrest, modify locally, fork or something else to fulfill your requirement.
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

### Conclusion

There are various groups of people that work with Helm. There might be a group of people concerned with maintaining and installing a specific chart to the best of their effort. In this case the regular Helm workflow might be suited well.

But there are also people who maintain and consume a larger number of charts which likely are overwhelmed by the various individual design approaches to creating Helm charts. For newcomers to this group, using the HULL library omits the quite tedious YAML template creation and placeholder logic by offering a simple interface to specifying objects directly.

But out of necessity, this initially group of people new to Kubernetes needs to get involved deeper in the design of individual helm charts to be able to understand how to configure them when following the regular Helm workflow. By that point you are also likely familiar with the Kubernetes API objects and YAML structures and feel closer to using this directly than rebuilding every API object property via the abstractions introduced by Helm charts. 

That is why HULL allows you out-of-the-box to specify complete Kubernetes objects and supports where possible to foster frequent usecases by a light abstraction layer.

## Components

At the core of the HULL library is the interplay between `values.yaml`, `values.schema.json`, `hull_init.yaml` and the template files in `/templates` that come with HULL.

### The `values.yaml`

For the HULL related functionalities only entries under the `hull` subkey are relevant. No other top level key is relevant for HULL so it can co-exist with any other Helm chart configuration properties.

### The `values.schema.json`

The `values.schema.json` of each HULL library release is built from the respective version of the Kubernetes API JSON Schema which is:
- extended with the HULL specific properties to provide the HULL specific functionalities and
- minor modifications to the strict K8S JSON schema to allow co-existence with the HULL specific properties.

This means that misconfigurations of the `values.yaml` `hull` subsection are either visible on input or catched on processing the chart.

### The `hull_init.yaml`

The `hull_init.yaml` needs to be placed in the parents charts `/templates` folder. It contains a loop over all handled object types and their specific configurational properties. Within the loop all objects of a handled type (as specified in `values.yaml`) are iterated over and the corresponding rendering function is called for the specified and enabled object. 

### The `/templates`

The templates folder in HULL contains only functions as it is mandatory for Helm library charts. 

---
Back to [README.md](./../README.md)