# Creating HorizontalPodAutoscaler

The HULL HorizontalPodAutoscaler object allows to reference a chart internal workload for autoscaling by simple key name. Any external workload name needs to be marked with `staticName: true`.

## JSON Schema Elements

### The `hull.HorizontalPodAutoscaler.v1` properties

Properties can be set as they are defined in the [Kubernetes API's horizontalpodautoscalerspec spec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#horizontalpodautoscalerspec-v2-autoscaling). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `scaleTargetRef.staticName` | Specifies whether the `name` key of this `scaleTargetRef` refers to a fixed name of an object the cluster or not. 
---
Back to [README.md](./../README.md)
