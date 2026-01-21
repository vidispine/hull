# _The `hull.objects` section_

The top-level object types beneath `hull.objects` represent the supported Kubernetes object types you might want to create instances from. Each object type is a dictionary where the entries values are the objects properties and each object has it's own key which is unique to the object type it belongs to. Further K8S object types can be added as needed to the library so it can easily be extended.

## _Keys of object instances_

One important aspect is that for all top-level object types, instances of a particular type are always identified by a key which is unique to the instance and object type combination. The same key can however be used for instances of different object types.

By having keys that identify instances you can:

- do multi-layered merging of object properties by stacking `values.yaml` files on top of each other. You might start with defining the default object structure of the application or micro service defined in the given helm chart. Then you might add a `values.yaml` layer for a particular environment like staging or production. Then you might add a `values.yaml` layer for credentials. And so on. By uniquely identifying the instances of a particular K8s object type it becomes easy to adjust the objects properties through a multitude of layers.
- use the key of an instance for naming the instance. All instance names are constructed by the following ground rule: `{{ printf "%s-%s-%s" .Release.Name .Chart.Name key }}`. This generates unique, dynamic names per object type and release + instance key combination.

  For example, assuming the parent Helm chart is named `my_webservice` and the release named `staging` and given this specification in `values.yaml`:

  ```yaml
    hull:
      objects:
        deployment:
          nginx:
            pod:
              containers:
                nginx:
                  repository: nginx
                  tag: 1.14.2
  ```

  a Kubernetes deployment object with the following `metadata.name` is created:

  `my_webservice-staging-nginx`

  > Note that you can opt to define a static name for instances you create by adding a property `staticName: true` to your objects definition. If you do so the objects name will exactly match the key name you chose.

- each particular instance can have an `enabled` sub-field set to `true` or `false`. This way you can predefine instances of object types in your helm charts `values.yaml` but not deploy them in a default scenario. Or enable them by default and refrain from deploying them in a particular environment by disabling them in an superimposed system specific `values.yaml`. Note that unless you explicitly specify `enabled: false` each instance you define will be created by default, a missing `enabled` key is equivalent to `enabled: true`.

- cross-referencing objects within a helm chart by the instance key is a useful feature of the HULL library. This is possible in these contexts:
  - when a reference to a ConfigMap or Secret comes into play you can just use the key of the targeted instance and the dynamic name will be rendered in the output. This is possible for referencing
    - a ConfigMap or Secret behind a Volume or
    - a Secret behind an Ingress' TLS specification or
    - a ConfigMap or Secret behind an environment value added to a container spec.
  - when referencing Services in the backend of an ingress' host you can specify the key to reference the backend service.
  
    > Note that you can in these cases opt to refer to a static name instead too. Adding a property `staticName: true` to the dictionary with your reference will force the referenced objects name to exactly match the name you entered.

## _Values of object instances_

The values of object instance keys reflects the Kubernetes objects to create for the chart. To specify these objects efficiently, the available properties for configuration can be split into three groups:

1. Basic HULL object configuration with [hull.ObjectBase.v1](/hull/files/doc/API/hull_objects_base.md) whose properties are available for all object types and instances. These are `enabled`, `staticName`, `annotations` and `labels`.

    Given the example of a `deployment` named `nginx` you can add the following properties of [hull.ObjectBase.v1](/hull/files/doc/API/hull_objects_base.md) to the object instance:

      ```yaml
      hull:
        objects:
          deployment:
            nginx: # unique key/identifier of the deployment to create
              staticName: true # property of hull.ObjectBase.v1
                              # forces the metadata.name to be just the <KEY> 'nginx' 
                              # and not a dynamic name '<CHART>-<RELEASE>-<KEY>' which 
                              # would be the better default behavior of creating 
                              # unique object names for all objects.
              enabled: true    # property of hull.ObjectBase.v1
                              # this deployment will be rendered to a YAML object if enabled
              labels:
                demo_label: "demo" # property of hull.ObjectBase.v1
                                  # add all labels here that shall be added 
                                  # to the object instance metadata section
              annotations:
                demo_annotation: "demo" # property of hull.ObjectBase.v1
                                        # add all annotations here that shall be added 
                                        # to the object instance metadata section
              pod: 
                ... # Here would come the hull.PodTemplate.v1 definition
                    # see below for details

      ```

2. Specialized HULL object properties for some object types. Below is a reference of which object type supports which special properties in addition to the basic object configuration.

    Again given the example of a `deployment` named `nginx` you would want to add properties of the HULL [**hull.PodTemplate.v1**](/hull/files/doc/API/hull_objects_pod.md) to the instance. With them you set the `pod` property to define the pod template (initContainers, containers, volumes, ...) and can add `templateLabels` and `templateAnnotations` just to the pods created `metadata` and not the deployment objects `metadata` section:

      ```yaml
      hull:
        objects:
          deployment:
            nginx: 
              staticName: true 
              enabled: true 
              labels: 
                demo_label: "demo" 
              annotations: 
                demo_annotation: "demo" 
              templateLabels: # property of hull.PodTemplate.v1 to define 
                              # labels only added to the pod
                demo_pod_label: "demo pod" 
              templateAnnotations: # property of hull.PodTemplate.v1 to define 
                              # annotations only added to the pod
                demo_pod_annotation: "demo pod"
              pod: # property of hull.PodTemplate.v1 to define the pod template
                containers:
                  nginx: # all containers of a pod template are also referenced by a 
                        # unique key to make manipulating them easy.
                    image:
                      repository: nginx # specify repository and tag
                                        # separately with HULL for easier composability
                      tag: 1.14.2
                    ... # further properties (volumeMounts, affinities, ...)

      ```

3. Kubernetes object properties. For each object type it is basically possible to specify all existing Kubernetes properties. In case a HULL property overwrites a identically named Kubernetes property the HULL property has precedence. Even if a HULL property overrides a Kubernetes property it is intended to provide the same complete configuration options, even if sometimes handled differently by HULL.

    Some of the typical top-level Kubernetes object properties and fields don't require setting them with HULL based objects because they can be deducted automatically:
    - the `apiVersion` and `kind` are determined by the HULL object type and Kubernetes API version and don't require to be explicitly set (except for objects of type `customresource`).
    - the top-level `metadata` dictionary on objects is handled by HULL via the `annotations` and `labels` fields and the naming rules explained above. So the `metadata` field does not require configuration and is hence not configurable for any object.

    Some lower level structures are also converted from the Kubernetes API array form to a dictionary form or are modified to improve working with them. This also enables more sophisticated merging of layers since arrays don't merge well, they only can be overwritten completely. Overwriting arrays however can make it hard to forget about elements that are contained in the default form of the array (you would need to know that they existed in the first place). In short, for a layered configuration approach without an endless amount of elements the dictionary is preferable for representing data since it offers a much better merging support.

    So again using the example of a `deployment` named `nginx` you can add the remaining available Kubernetes properties to the object instance which are not handled by HULL as shown below. For a `deployment` specifically you can add all the remaining properties defined in the `deploymentspec` API schema from [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#deploymentspec-v1-apps) which are `minReadySeconds`, `paused`, `progressDeadlineSeconds`, `replicas`, `revisionHistoryLimit` and `strategy`. If properties are marked as mandatory in the Kubernetes JSON schema you must provide them otherwise the rendering process will fail:

      ```yaml
      hull:
        objects:
          deployment:
            nginx: 
              staticName: true 
              enabled: true 
              labels: 
                demo_label: "demo" 
              annotations: 
                demo_annotation: "demo" 
              pod:
                ... # Here would come the hull.PodTemplate.v1 definition
                    # see above for details 
              replicas: 3 # property from the Kubernetes API deploymentspec
              strategy: # property from the Kubernetes API deploymentspec
                type: Recreate
              ... # further Kubernetes API deploymentspec options

      ```

## _Composing objects with HULL_

Here is an overview of which top level properties are available for which object type in HULL. The HULL properties are grouped by the respective HULL JSON schema group they belong to. A detailed description of these groups and their properties is found in the documentation of this helm chart and the respective linked documents.

### **[Workloads APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-workloads-apis-strong-)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------------------- |
| `deployment` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](/hull/files/doc/API/hull_objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#deploymentspec-v1-apps)<br>`minReadySeconds`<br>`paused`<br>`progressDeadlineSeconds`<br>`replicas`<br>`revisionHistoryLimit`<br>`strategy` |
| `job` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](/hull/files/doc/API/hull_objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**jobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#jobspec-v1-batch)<br>`activeDeadlineSeconds`<br>`backoffLimit`<br>`completionMode`<br>`completions`<br>`manualSelector`<br>`parallelism`<br>`selector`<br>`suspend`<br>`ttlSecondsAfterFinished` |
| `daemonset` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](/hull/files/doc/API/hull_objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**daemonsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#daemonsetspec-v1-apps)<br>`minReadySeconds`<br>`ordinals`<br>`revisionHistoryLimit`<br>`updateStrategy` |
| `statefulset` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.PodTemplate.v1**](/hull/files/doc/API/hull_objects_pod.md)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**statefulsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#statefulsetspec-v1-apps)<br>`podManagementPolicy`<br>`replicas`<br>`revisionHistoryLimit`<br>`serviceName`<br>`updateStrategy`<br>`serviceName`<br>`volumeClaimTemplates` |
| `cronjob` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Job.v1**](./README.md)<br>`job` | [**cronjobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#cronjobspec-v1-batch)<br>`concurrencyPolicy`<br>`failedJobsHistoryLimit`<br>`schedule`<br>`startingDeadlineSeconds`<br>`successfulJobsHistoryLimit`<br>`suspend` |

### **[Service APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-service-apis-strong-)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------- |
| `endpoints`<br>(deprecated<br>since<br>K8S 1.33) | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**endpoints-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#endpoints-v1-core)<br>`subsets` |
| `endpointslice` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**endpointslice-v1-discovery-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#endpointslice-v1-discovery-k8s-io)<br>`addressType`<br>`endpoints`<br>`ports` |
| `service` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Service.v1**](/hull/files/doc/API/hull_objects_service.md)<br>`ports` | [**servicespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#servicespec-v1-core)<br>`allocateLoadBalancerNodePorts`<br>`clusterIP`<br>`clusterIPs`<br>`externalIPs`<br>`externalName`<br>`externalTrafficPolicy`<br>`healthCheckNodePort`<br>`internalTrafficPolicy`<br>`ipFamilies`<br>`ipFamilyPolicy`<br>`loadBalancerClass`<br>`loadBalancerIP`<br>`loadBalancerSourceRanges`<br>`publishNotReadyAddresses`<br>`selector`<br>`sessionAffinity`<br>`sessionAffinityConfig`<br>`topologyKeys`<br>`type` |
| `ingress` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Ingress.v1**](/hull/files/doc/API/hull_objects_ingress.md)<br>`tls`<br>`rules` | [**ingressspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#ingressspec-v1-networking-k8s-io)<br>`defaultBackend`<br>`ingressClassName` |
| `ingressclass` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ingressclassspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#ingressclassspec-v1-networking-k8s-io)<br>`controller`<br>`parameters` |

### **[Config and Storage APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-config-and-storage-apis-strong-)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------------------- |
| `configmap` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](/hull/files/doc/API/hull_objects_configmaps_secrets.md)<br>`data` | [**configmap-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#configmap-v1-core)<br>`binaryData`<br>`immutable` |
| `secret` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](/hull/files/doc/API/hull_objects_configmaps_secrets.md)<br>`data` | [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#secret-v1-core)<br>`immutable`<br>`stringData`<br>`type` |
| `registry` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Registry.v1**](/hull/files/doc/API/hull_objects_registry.md)<br>`server`<br>`username`<br>`password` | [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#secret-v1-core) |
| `persistentvolumeclaim` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**persistentvolumeclaimspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#persistentvolumeclaimspec-v1-core)<br>`accessModes`<br>`dataSource`<br>`resources`<br>`selector`<br>`storageClassName`<br>`volumeMode`<br>`volumeName` |
| `storageclass` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**storageclass-v1-storage-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#storageclass-v1-storage-k8s-io)<br>`allowVolumeExpansion`<br>`allowedTopologies`<br>`mountOptions`<br>`parameters`<br>`provisioner`<br>`reclaimPolicy`<br>`volumeBindingMode` |

### **[Metadata APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-metadata-apis-strong-)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------------------- |
| `customresource` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.CustomResource.v1**](/hull/files/doc/API/hull_objects_customresource.md)<br>`apiVersion`<br>`kind`<br>`spec` | |
| `limitrange` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**limitrange-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#limitrange-v1-core)<br>`limits` |
| `horizontalpodautoscaler` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.HorizontalPodAutoscaler.v1**](/hull/files/doc/API/hull_objects_horizontalpodautoscaler.md)<br>`scaleTargetRef` | [**horizontalpodautoscalerspec-v2-autoscaling**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#horizontalpodautoscalerspec-v2-autoscaling)<br>`behavior`<br>`maxReplicas`<br>`metrics`<br>`minReplicas` |
| `mutatingwebhookconfiguration` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.MutatingWebhook.v1**](/hull/files/doc/API/hull_objects_webhook.md)<br>`webhooks` | |
| `poddisruptionbudget` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**poddisruptionbudgetspec-v1-policy**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#poddisruptionbudgetspec-v1-policy)<br>`maxUnavailable`<br>`minAvailable`<br>`selector`<br>`unhealthyPodEvictionPolicy` |
| `validatingwebhookconfiguration` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.ValidatingWebhook.v1**](/hull/files/doc/API/hull_objects_webhook.md)<br>`webhooks` | |
| `priorityclass` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**priorityclass-v1-scheduling-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#priorityclass-v1-scheduling-k8s-io)<br>`description`<br>`globalDefault`<br>`preemptionPolicy`<br>`value` |

### **[Cluster APIs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#-strong-cluster-apis-strong-)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------------------- |
| `clusterrole` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Rule.v1**](/hull/files/doc/API/hull_objects_role.md)<br>`rules` | [**clusterrole-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#clusterrole-v1-rbac-authorization-k8s-io)<br>`aggregationRule` |
| `clusterrolebinding` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**clusterrolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#clusterrolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects` |
| `namespace` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**namespace-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#namespace-v1-core)<br>`spec`<br>`status` |
| `persistentvolume` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**persistentvolumespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#persistentvolumespec-v1-core)<br>`accessModes`<br>`awsElasticBlockStore`<br>`azureDisk`<br>`azureFile`<br>`capacity`<br>`cephfs`<br>`cinder`<br>`claimRef`<br>`csi`<br>`fc`<br>`flexVolume`<br>`flocker`<br>`gcePersistentDisk`<br>`glusterfs`<br>`hostPath`<br>`iscsi`<br>`local`<br>`mountOptions`<br>`nfs`<br>`nodeAffinity`<br>`persistentVolumeReclaimPolicy`<br>`photonPersistentDisk`<br>`portworxVolume`<br>`quobyte`<br>`rbd`<br>`scaleIO`<br>`storageClassName`<br>`storageos`<br>`volumeMode`<br>`vsphereVolume` |
| `role` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Rule.v1**](/hull/files/doc/API/hull_objects_role.md)<br>`rules` | [**role-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#role-v1-rbac-authorization-k8s-io) |
| `rolebinding` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**rolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#rolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects` |
| `serviceaccount` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**serviceaccount-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#serviceaccount-v1-core)<br>`automountServiceAccountToken`<br>`imagePullSecrets`<br>`secrets` |
| `resourcequota` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**resourcequotaspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#resourcequotaspec-v1-core)<br>`hard`<br>`scopeSelector`<br>`scopes` |
| `networkpolicy` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**networkpolicyspec-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#networkpolicyspec-v1-networking-k8s-io)<br>`egress`<br>`ingress`<br>`podSelector`<br>`policyTypes` |

### **[Gateway APIs](https://gateway-api.sigs.k8s.io/reference/spec/#api-specification)**

| HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
| ------------------------------ | ------------------- | ---------------------------------- |
| `backendlbpolicy` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.BackendLBPolicy.v1alpha2**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`targetRefs` | [**backendlbpolicyspec-v1alpha2-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.BackendLBPolicySpec)<br>`sessionPersistence` |
| `backendtlspolicy` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.BackendTLSPolicy.v1alpha3**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`targetRefs` | [**backendtlspolicyspec-v1alpha3-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha3.BackendTLSPolicySpec)<br>`options`<br>`validation` |
| `gatewayclass` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**gatewayclassspec-v1-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewayClassSpec)<br>`controllerName`<br>`description`<br>`parametersRef` |
| `gateway` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Gateway.v1**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`addresses`<br>`listeners` | [**gatewayspec-v1-gateway-networking-k8s-io**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewaySpec)<br>`backendTLS`<br>`gatewayClassName`<br>`infrastructure` |
| `grpcroute` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.GRPCRoute.v1**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules` | |
| `httproute` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.HTTPRoute.v1**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules` | |
| `referencegrant` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.ReferenceGrant.v1beta1**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`from`<br>`to` | |
| `tcproute` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.TCPRoute.v1alpha2**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`parentRefs`<br>`rules` | |
| `tlsroute` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.TLSRoute.v1alpha2**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`hostnames`<br>`parentRefs`<br>`rules` | |
| `udproute` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.UDPRoute.v1alpha2**](/hull/files/doc/API/hull_objects_gateway_api.md)<br>`parentRefs`<br>`rules` | |

### **Other APIs**

HULL<br> Object Type<br>&#160; | HULL <br>Properties | Kubernetes/External<br> Properties |
------------------------------ | ------------------ -| ---------------------------------- |
`servicemonitor` | [**hull.ObjectBase.v1**](/hull/files/doc/API/hull_objects_base.md)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ServiceMonitor CRD**](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/crds/crd-servicemonitors.yaml)<br>`spec`
