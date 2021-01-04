# HULL Objects

When defining Kubernetes objects via HULL a ground set of configuration options is available for all objects. These are explained below. In addition to this, the full stack of configuration options for a matching Kubernetes API object is provided for each type, whereas for some object types there is additional functionality provided by the HULL library to improve configuration which is then overriding the API properties definitions.

## General object configuration

First of, all objects are created under their respective object type's key under `hull.objects`. As of now, the following object keys are supported:

- `configmap` 
- `secret`
- `registry`
- `deployment`
- `job`
- `daemonset`
- `statefulset`
- `cronjob`
- `serviceaccount`
- `role`
- `rolebinding`
- `clusterrole`
- `clusterrolebinding`
- `storageclass`
- `persistentvolume`
- `persistentvolumeclaim`
- `service`
- `ingress`
- `customresource`
- `servicemonitor`

Each object type is a dictionary where the entries values are the objects properties and each object has it's own key which is unique to the object type. The object keys play an important role in naming the Kubernetes objects. By default the object key provides the actual objects name in Kubernetes `metadata.name` combined with chart and release name.

For example, assuming the parent Helm chart is named `my_webservice` and the release named `staging` and given this specification:

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

    my_webservice-staging-nginx

The further keys available for base specifications ([**hull.ObjectBase.v1**](./../values.schema.json) in [values.schema.json](./../values.schema.json)) are:

- `staticName`: 
  
  A boolean switch. If set to true the object does not get a dynamically created name (see above) assigned but a name that only consists of the key name. Given the above example the `metadata.name` field will be `nginx` if `staticName` is set to true. 
  Using static names is helpful in case you need to address the object from another Kubernetes object that is not part of the Helm chart and hence you want to refer to a fixed object name. 

- `enabled`: 

  A boolean switch. If set to true or missing, the object will be rendered for deployment. If set to false, it will be omitted. This way you can predefine objects which are only enabled and in certain environments when needed. 

- `labels`: 

  Dictionary with labels to add to the Kubernetes objects main `metadata.labels` section.

- `annotations`: 

  Dictionary with annotations to add to the Kubernetes objects main `metadata.annotations` section

## Kubernetes API object properties

Besides using these options which are usable for all HULL objects you typically have the matching Kubernetes object specific properties at your disposal for configuration. Some of the typical top-level Kubernetes object properties and fields don't require setting them with HULL based objects or are overriden by properties of the HULL objects:
- `apiVersion` and `kind` are determined by the HULL object type and don't require setting (except for `customresources`)
- `metadata` on objects is handled by HULL (via the `annotations` and `labels` fields and the naming rules) so the `metadata` field does not require configuration and is not configurable for any object. 
- For pod-based objects there typically exist the following properties in the top-level `template` section which don't require setting and are handled by HULL:
  - `template` properties on objects can be left out, the proper objects structure is created automatically under the hood. Labels and annotations for the `template` section can be set directly with `templateAnnotations` and `templateLabels`
  - `selector` is auto created to match the objects main metadata (except for `services` where the selector field can be overwritten)

Here is an overview of which top level properties are available for which object type in HULL. The HULL properties are grouped by the respective HULL JSON schema group they belong to. A detailed description of these groups and their properties is found in the documentation of this helm chart. For all properties inherited from the Kubernetes API refer to the linked API reference documentation on the object for usage and restrictions:

HULL<br> object type<br>&#160; | HULL <br>properties | Kubernetes/External<br> properties
------------------------------- | -----------------------------| -----------------------------------------| -----------------|
`configmap` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](./../values.schema.json)<br>`data` |  [**configmap-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#configmap-v1-core)<br>`binaryData`<br>`immutable` | |
`secret` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.VirtualFolder.v1**](./../values.schema.json)<br>`data` |  [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#secret-v1-core)<br>`immutable`<br>`stringData`<br>`type` |
`registry` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Registry.v1**](./../values.schema.json)<br>`server`<br>`username`<br>`password` | [**secret-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#secret-v1-core)
`deployment` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Pod.v1**](./../values.schema.json)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**deploymentspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#deploymentspec-v1-apps)<br>`minReadySeconds`<br>`paused`<br>`progressDeadlineSeconds`<br>`replicas`<br>`revisionHistoryLimit`<br>`strategy` |
`job` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Pod.v1**](./../values.schema.json)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**jobspec-v1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#jobspec-v1-batch)<br>`activeDeadlineSeconds`<br>`backoffLimit`<br>`completions`<br>`manualSelector`<br>`parallelism`<br>`ttlSecondsAfterFinished` |
`daemonset` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Pod.v1**](./../values.schema.json)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**daemonsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#daemonsetspec-v1-apps)<br>`minReadySeconds`<br>`revisionHistoryLimit`<br>`updateStrategy` | 
`statefulset` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Pod.v1**](./../values.schema.json)<br>`templateAnnotations`<br>`templateLabels`<br>`pod` | [**statefulsetspec-v1-apps**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#statefulsetspec-v1-apps)<br>`podManagementPolicy`<br>`replicas`<br>`revisionHistoryLimit`<br>`updateStrategy`<br>`serviceName`<br>`volumeClaimTemplates` |
`cronjob` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Job.v1**](./../values.schema.json)<br>`job` | [**cronjobspec-v1beta1-batch**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#cronjobspec-v1beta1-batch)<br>`concurrencyPolicy`<br>`failedJobsHistoryLimit`<br>`schedule`<br>`startingDeadlineSeconds`<br>`successfulJobsHistoryLimit`<br>`suspend` | 
`serviceaccount` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**serviceaccount-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#serviceaccount-v1-core)<br>`automountServiceAccountToken`<br>`imagePullSecrets`<br>`secrets` | 
`role` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**role-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#role-v1-rbac-authorization-k8s-io)<br>`rules` | 
`rolebinding` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**rolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#rolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects` | 
`clusterrole` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**clusterrole-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#clusterrole-v1-rbac-authorization-k8s-io)<br>`aggregationRule`<br>`rules` | 
`clusterrolebinding` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**clusterrolebinding-v1-rbac-authorization-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#clusterrolebinding-v1-rbac-authorization-k8s-io)<br>`roleRef`<br>`subjects` | 
`storageclass` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**storageclass-v1-storage-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#storageclass-v1-storage-k8s-io)<br>`allowVolumeExpansion`<br>`allowedTopologies`<br>`mountOptions`<br>`parameters`<br>`provisioner`<br>`reclaimPolicy`<br>`volumeBindingMode` | 
`persistentvolume` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#persistentvolumespec-v1-core)<br>`accessModes`<br>`awsElasticBlockStore`<br>`azureDisk`<br>`azureFile`<br>`capacity`<br>`cephfs`<br>`cinder`<br>`claimRef`<br>`csi`<br>`fc`<br>`flexVolume`<br>`flocker`<br>`gcePersistentDisk`<br>`glusterfs`<br>`hostPath`<br>`iscsi`<br>`lcal`<br>`mountOptions`<br>`nfs`<br>`nodeAffinity`<br>`persistentVolumeReclaimPolicy`<br>`photonPersistentDisk`<br>`portworxVolume`<br>`quobyte`<br>`rbd`<br>`scaleIO`<br>`storageClassName`<br>`storageos`<br>`volumeMode`<br>`vsphereVolume`| 
`persistentvolumeclaim` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` |  [**persistentvolumeclaimspec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#persistentvolumeclaimspec-v1-core)<br>`accessModes`<br>`dataSource`<br>`resources`<br>`selector`<br>`storageClassName`<br>`volumeMode`<br>`volumeName` | 
`service` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Service.v1**](./../values.schema.json)<br>`ports` | [**servicespec-v1-core**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#servicespec-v1-core)<br>`clusterIP`<br>`externalIPs`<br>`externalName`<br>`externalTrafficPolicy`<br>`healthCheckNodePort`<br>`ipFamily`<br>`loadBalancerIP`<br>`loadBalancerSourceRanges`<br>`publishNotReadyAddresses`<br>`selector`<br>`sessionAffinity`<br>`sessionAffinityConfig`<br>`topologyKeys`<br>`type` | 
`ingress` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.Ingress.v1**](./../values.schema.json)<br>`tls`<br>`rules` | [**ingressclass-v1-networking-k8s-io**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#ingressclass-v1-networking-k8s-io)<br>`backend`<br>`ingressClassName` | 
`customresource` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName`<br><br>[**hull.CustomResource.v1**](./../values.schema.json)<br>`apiVersion`<br>`kind`<br>`spec` | | 
`servicemonitor` | [**hull.ObjectBase.v1**](./../values.schema.json)<br>`enabled`<br>`annotations`<br>`labels`<br>`staticName` | [**ServiceMonitor CRD**](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/crds/crd-servicemonitors.yaml)<br>`spec` | 

---
Back to [README.md](./../README.md)