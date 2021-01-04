# Metadata

We can add custom metadata besides the standard metadata which is always auto-created. The custom metadata labels and annotations can be applied to either all objects within a helm chart, all objects of a given type or just individual objects. 

The following `values.yaml` showcases all possibilities to set metadata:

```yaml
hull:
  config:
    general:       
      metadata:
        labels:         
          custom: # Add some custom labels to all objects created in this chart
            general_custom_label_1: General Custom Label 1
            general_custom_label_2: General Custom Label 2
            general_custom_label_3: General Custom Label 3
        annotations: 
          custom: # Add some custom annotations to all objects created in this chart
            general_custom_annotation_1: General Custom Annotation 1
            general_custom_annotation_2: General Custom Annotation 2
            general_custom_annotation_3: General Custom Annotation 3    
  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_: # this object key is used to set defaults per object type
        annotations:
          default_annotation_1:  Default Annotation 1
          default_annotation_2:  Default Annotation 2
          general_custom_annotation_3: Default Annotation 3 # overwrite the global default
        labels:
          default_label_1:  Default Label 1
          default_label_2:  Default Label 2
          general_custom_label_3: Default Label 3 # overwrites the global default
      nginx: # specify the nginx deployment under key 'nginx'
        pod:
          replicas: 3
          containers:
            nginx:
              repository: nginx
              tag: 1.14.2
```

The outcome will be a K8S deployment object being deployed to the cluster that looks like this (the ServiceAccount is left out):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    default_annotation_1: Default Annotation 1
    default_annotation_2: Default Annotation 2
    general_custom_annotation_1: General Custom Annotation 1
    general_custom_annotation_2: General Custom Annotation 2
    general_custom_annotation_3: Default Annotation 3
  labels:
    app.kubernetes.io/component: nginx
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: hull-test
    app.kubernetes.io/part-of: undefined
    app.kubernetes.io/version: "1"
    default_label_1: Default Label 1
    default_label_2: Default Label 2
    general_custom_label_1: General Custom Label 1
    general_custom_label_2: General Custom Label 2
    general_custom_label_3: Default Label 3
    helm.sh/chart: hull-test-1
  name: release-name-hull-test-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/component: nginx
      app.kubernetes.io/instance: RELEASE-NAME
      app.kubernetes.io/name: hull-test
  template:
    metadata:
      annotations:
        default_annotation_1: Default Annotation 1
        default_annotation_2: Default Annotation 2
        general_custom_annotation_1: General Custom Annotation 1
        general_custom_annotation_2: General Custom Annotation 2
        general_custom_annotation_3: Default Annotation 3
      labels:
        app.kubernetes.io/component: nginx
        app.kubernetes.io/instance: RELEASE-NAME
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: hull-test
        app.kubernetes.io/part-of: undefined
        app.kubernetes.io/version: "1"
        default_label_1: Default Label 1
        default_label_2: Default Label 2
        general_custom_label_1: General Custom Label 1
        general_custom_label_2: General Custom Label 2
        general_custom_label_3: Default Label 3
        helm.sh/chart: hull-test-1
    spec:
      containers:
      - env: []
        envFrom: []
        image: nginx:1.14.2
        name: nginx
        ports: []
        volumeMounts: []
      initContainers: []
      serviceAccountName: release-name-hull-test-default
      volumes: []
```