# Adding the HULL library chart to a Helm chart

To add the HULL library chart to a Helm chart you need to:

- follow the basic instructions on [how to add library charts to a Helm chart](https://helm.sh/docs/topics/library_charts/). 

  When adding the HULL library chart, choose a version that fits your targeted Kubernetes API versions best. The HULL chart version matches the implmemented Kubernetes API version that is used for validation, so it should be at least the minimum version of the cluster(s) you target.

- from the HULL library chart you included, you need to copy the file named `hull_init.yaml` from the HULL charts root folder to your parent charts `/templates` folder. 

  **This is required to have the HULL library functions render the objects specified under the key `hull.objects` in the parent chart!**

If these preliminary steps have been taken you can start using the HULL chart to render Kubernetes objects without having to deal with the templating boilerplate YAML.

---
Back to [README.md](./../README.md)
