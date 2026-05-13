# Combining HULL with regular Helm charts

If you have added HULL to your Helm chart, some advanced options open up which allow to combine the HULL workflow with additional Helm templates or subcharts. The following sections aim to give an overview of what is possible.

## Using additional templates with HULL

See the below flow for the difference between regular object rendering using template files and the HULL-based object rendering from a modified `values.yaml`:

```code
                      /templates            output       
                                                         
                                                         
                    ┌─────────────┐       ┌─────────────┐
                    │  hull.yaml  │       │  hull.yaml  │
                    │             │       │             │
   read & transform │ ┌───────┐   │       │             │
        ┌───────────│─┼trigger│   │       │             │
┌───────▼────────┐  │ └───────┘   │       │             │
│                │  │             │       │  ┌───────┐  │
│  values.yaml   │  │             │       │  │ YAML  │  │
│                │  │             │       │  └──▲────┘  │
└───────┬────────┘  │             │       │     │       │
        │           │             │       │     │       │
        │           │             │       │     │       │
        └───────────┼─────────────┼───────┼─────┘       │
    write objects   │             │       │             │
                    └─────────────┘       └─────────────┘
                    ┌─────────────┐       ┌─────────────┐
                    │  redis.yaml │       │  redis.yaml │
┌────────────────┐  │             │       │             │
│                │  │ ┌───────┐   │ adapt │  ┌───────┐  │
│  values.yaml   │  │ │ YAML  ┼───┼───────┼──► YAML  │  │
│                │  │ └──┬────┘   │       │  └───────┘  │
└───────▲────────┘  │    │        │       │             │
        │           └────┼────────┘       └─────────────┘
        │ read values    │
        └────────────────┘
```

Within [the in-depth analysis](https://github.com/vidispine/hull/issues/367) of the topic it became obvious, that during rendering process of HULL, the Helm charts `.Values` context is manipulated in memory and remains in the manipulated state if templates are processed after `hull.yaml`.

Helm reads in the templates it finds in the `/templates` folder in a defined order. Template files that are placed in folders are read before those that are directly placed in `/templates` and generally the files are read in reverse alphanumerical fashion.

Utilizing this knowledge of the processing order - and the fact, that executing the `hull.yaml` changes the `.Values` for all templates being read afterwards - it is possible to inject HULL functionality into regular templates.

Note that, if you plan to add templates to a HULL based chart, you should copy the `hull.yaml` not to the `/templates` folder directly but within a subfolder that comes last in alphanumerical order (recommended is `/template/zzz/hull.yaml`). This way it is guaranteed to be read first.

An example HULL-based chart setup could look like this:

```code
| README.md
| Chart.yaml
| values.yaml
| charts
|-| hull
| templates
|-| gateway.yaml
|-| zzz
|-|-| hull.yaml
```

In detail, the setup contains a HULL based chart with an additional template `gateway.yaml`:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    api-approved.kubernetes.io: https://github.com/kubernetes-sigs/gateway-api/pull/3328
    gateway.networking.k8s.io/bundle-version: v1.3.0
    gateway.networking.k8s.io/channel: experimental
  creationTimestamp: null
  name: referencegrants.gateway.networking.k8s.io
spec:
  group: gateway.networking.k8s.io
  names:
    categories:
    - gateway-api
    kind: ReferenceGrant
    listKind: ReferenceGrantList
    plural: referencegrants
    shortNames:
    - refgrant
    singular: referencegrant
  scope: Namespaced
  versions:
  - additionalPrinterColumns:
    - jsonPath: .metadata.creationTimestamp
      name: Age
      type: date
    name: v1beta1
    schema:
      openAPIV3Schema:
        description: |-
          ReferenceGrant identifies kinds of resources in other namespaces that are
          trusted to reference the specified kinds of resources in the same namespace
          as the policy.

          Each ReferenceGrant can be used to represent a unique trust relationship.
          Additional Reference Grants can be used to add to the set of trusted
          sources of inbound references for the namespace they are defined within.

          All cross-namespace references in Gateway API (with the exception of cross-namespace
          Gateway-route attachment) require a ReferenceGrant.

          ReferenceGrant is a form of runtime verification allowing users to assert
          which cross-namespace object references are permitted. Implementations that
          support ReferenceGrant MUST NOT permit cross-namespace references which have
          no grant, and MUST respond to the removal of a grant by revoking the access
          that the grant allowed.
        properties:
          apiVersion:
            description: |-
              APIVersion defines the versioned schema of this representation of an object.
              Servers should convert recognized schemas to the latest internal value, and
              may reject unrecognized values.
              More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
            type: string
            default: {{ .Values.hull.config.specific.the_value_target }}
```

The minimal example `values.yaml` has this content:

```yaml
hull:
  config:
    specific:
      the_version_source: 1.2.3.4.5
      the_value_target: _HT*hull.config.specific.the_version_source
```

Assuming that the presence of the `zzz/hull.yaml` file has no effect on rendering `gateway.yaml`, the last line is expected to be resolved to the unprocessed reference it points to:

```yaml
            default: _HT*hull.config.specific.the_version_source
```

However, with included `zzz/hull.yaml` the outcome of the last line in `gateway.yaml` changes to:

```yaml
            default: 1.2.3.4.5
```

This means that the source `.Values` have been manipulated by the functions triggered in `zzz/hull.yaml` so that the HULL transformation `_HT*hull.config.specific.the_version_source` has been transformed to the actual value the Get transformation points too.

Using this method it becomes possible now to put HULL logic into the `values.yaml` fields and to utilize it by referencing them.

## Using additional subcharts with HULL

The power of HULL transformations can also be extended to subcharts included in a HULL based parent chart to a certain degree.

In general, Helm strictly prevents access to a parent charts context when a subchart is rendered. The notable exception to this rule is the `global` key in the `values.yaml`. By design, all properties put under the `global` key are accessible by subcharts at the same key under `global`. In other words, when handing over the subchart context to the subchart rendering process, the `global` dictionary is added to the subcharts `.Values` context.

Importantly though, any manipulation done via `hull.yaml` functions in the parent chart (as described in the previous chapter), is not being passed to the subchart's `.Values` when the subchart is rendered. Presumably this is due to the fact that Helm evaluates subcharts before the parent chart so the `hull.yaml` cannot manipulate the data being passed.

The caveat is, To enable HULL processing within a subchart, it is required to add the `zzz/hull.yaml` folder and file to the subchart `/templates` in the same manner as in the previous scenario. If that is possible, the rendering of HULL transformations is activated for the subchart.

The scope of transformations within a subchart is local to the subchart as mentioned but includes access to fields in the `global` scope as well, allowing to use parent- and subchart wide logic when it the logic is constrained to the `global` section.

**Note that it is not needed to add the `hull` chart as a dependency to your subcharts, the presence as a dependency of the parent chart is sufficient. The reason is that `hull.yaml` only triggers functions and the scope of functions is always global. Therefore, all functions can be called from the parents `hull` depencency when triggered in a subchart.**

To illustrate this with a full example, consider the following parent and two subcharts layout:

```code
| README.md
| Chart.yaml
| values.yaml
| charts
|-| hull
|-| kube-state-metrics
|-|-| templates
|-|-|-| zzz
|-|-|-|-| hull.yaml
|-| prometheus-postgres-exporter
|-|-| templates
|-|-|-| zzz
|-|-|-|-| hull.yaml
| templates
|-| hull.yaml
```

This example includes the [`kube-state-metrics`](https://artifacthub.io/packages/helm/prometheus-community/kube-state-metrics) and [`prometheus-postgres-exporter`](https://artifacthub.io/packages/helm/prometheus-community/prometheus-postgres-exporter) Helm charts as random real-life subchart examples. Both charts have been modified by inclusion of the `/templates/zzz/hull.yaml` as described.

The `values.yaml` contains the following lines:

```yaml
###################################################
### CONFIG
global:
  service_type: NodePort
  number_111: 111
  number_222: 222
  number_333: 333
  ref_number: _HT*global.another_number
  another_number: 333
  boolean_true: true
  an_ip: 123.345.431.543
  test_annotations:
    annotation_1: Global Annotation 1
    annotation_2: Global Annotation 2

kube-state-metrics:
  test_number: 999
  ip_number: _HT*global.an_ip
  local_type: LoadBalancer
  service:
    annotations: _HT*global.test_annotations
    type: _HT*global.service_type
    port: _HT*global.ref_number
    clusterIP: _HT*ip_number
    ipDualStack: 
      enabled: _HT*global.boolean_true


prometheus-postgres-exporter:
  local_type: LoadBalancer
  local_annotations:
    annotation_3: Local Annotation 1
    annotation_4: Local Annotation 2
  service: 
    annotations: |-
      _HT!
        {
          {{ $annot := _HT*global.test_annotations | merge _HT*local_annotations }}
          {{ range $key, $value := $annot }}
          {{ $key }}: {{ $value }},
          {{ end }} 
        }
    type: _HT*local_type
    port: _HT*global.ref_number
    targetPort: _HT*global.number_333

hull:
  config:
    specific:
      boolean_true: _HT*global.boolean_true
      new_port: _HT*global.number_111
      fixed_number: 12345
  ###################################################
          
  ###################################################
  ### OBJECTS
  objects:
    
  # INGRESS
    ingress:
      
      test-global:
        rules:
          first_host:
            host: host.one.com
            http:              
              paths:                  
                standard:
                  path: /standard
                  pathType: ImplementationSpecific
                  backend:
                    service:
                      name: service1_standard
                      port: 
                        number: _HT*hull.config.specific.new_port
```

After `helm template`'ing the Helm chart the following files are part of the rendered output. Each highligted file comes with an explanation of how and why the structures were created as they are:

1. `kube-state-metrics/templates/service.yaml`
  
    ```yaml
    ---
    # Source: hull-test/charts/kube-state-metrics/templates/service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: release-name-kube-state-metrics
      namespace: default
      labels:    
        helm.sh/chart: kube-state-metrics-7.1.0
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/component: metrics
        app.kubernetes.io/part-of: kube-state-metrics
        app.kubernetes.io/name: kube-state-metrics
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/version: "2.18.0"
      annotations:
        prometheus.io/scrape: 'true'
        annotation_1: Global Annotation 1
        annotation_2: Global Annotation 2
    spec:
      type: "NodePort"
      ipFamilies: 
        - IPv6
        - IPv4
      ipFamilyPolicy: PreferDualStack
      ports:
      - name: http
        protocol: TCP
        port: 333
        targetPort: http
      
      clusterIP: "123.345.431.543"
      selector:    
        app.kubernetes.io/name: kube-state-metrics
        app.kubernetes.io/instance: release-name
    ```
  
    Explanation:

    - the `spec.port` has value 333 from source field `global.another_number` as the result of accessing field `_HT*global.ref_number` where field `global.ref_number` itself references `_HT*global.another_number`. Two redirections have been processed to obtain the actual rendered value.  
    - the `spec.clusterIP` has also been resolved via indirection to the subchart local property `_HT*ip_number` which in turns access `global` field `an_ip`
    - the `metadata.annotations` are retrieved from `global` `annotations` dictionary.
    - the `spec.type` was set accessing subchart local property `local_type`
    - the `spec.ipFamilies` and `spec.ipFamilyPolicy` fields have been created by evaluation of the `_HT*global.boolean_true` field reference in the `kube-state-metrics.service.ipDualStack.enabled` property.

2. `prometheus-postgres-exporter/templates/service.yaml`

    ```yaml
    ---
    # Source: hull-test/charts/prometheus-postgres-exporter/templates/service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: release-name-prometheus-postgres-exporter
      namespace: default
      annotations:
        annotation_1: Global Annotation 1
        annotation_2: Global Annotation 2
        annotation_3: Local Annotation 1
        annotation_4: Local Annotation 2
      labels:
        helm.sh/chart: prometheus-postgres-exporter-7.0.0
        app.kubernetes.io/name: prometheus-postgres-exporter
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/version: "v0.17.1"
    spec:
      type: LoadBalancer
      ports:
        - port: 333
          targetPort: 333
          protocol: TCP
          name: http
      selector:
        app.kubernetes.io/name: prometheus-postgres-exporter
        app.kubernetes.io/instance: release-name

    ```

    Explanation:

    - the `spec.port` has value 333 from source field `global.another_number` as the result of accessing field `_HT*global.ref_number` where field `global.ref_number` itself references `_HT*global.another_number`. Two redirections have been processed to obtain the actual rendered value.
    - the `spec.targetPort` has value 333 from source field `global.number_333` as the result of accessing field `_HT*global.number_333`.  
    - the `metadata.annotations` are retrieved from merging the entries of `global.test_annotations` dictionary with the subchart local `local_annotations` dictionary.
    - the `spec.type` was set accessing subchart local property `local_type`

3. `hull.yaml` (excerpt)

    ```yaml
    ---
    # Source: hull-test/templates/hull.yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      labels:
        app.kubernetes.io/component: test-global
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: 1.36.0
        helm.sh/chart: hull-test-1.36.0
      name: release-name-hull-test-test-global
      namespace: default
    spec:
      rules:
      - host: host.one.com
        http:
          paths:
          - backend:
              service:
                name: release-name-hull-test-service1_standard
                port:
                  number: 111
            path: /standard
            pathType: ImplementationSpecific
    ```

    Explanation:

    - the `port.number` field has inherited value ´111´ from first accessing `hull.config.specific.new_port` which further references `global.number_111` for the actual integer value.

To summarize, the examples above demonstrates various possibilities how the HULL mechanism can help foster efficient chart configuration even in the context of regular Helm templates or subcharts. 