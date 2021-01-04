# Adding the HULL library chart to a Helm chart

To add the HULL library chart to a Helm chart you need to:
- follow the basic instructions on how to add [library charts](https://helm.sh/docs/topics/library_charts/) to a Helm chart. Choose the HULL library chart version that fits your targeted Kubernetes API versions best.
- from the chart you included, copy the file named `hull_init.yaml` to your parent charts `/temnplates` folder. This is required to have the HULL functions at your disposal.
