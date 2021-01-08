# Adding the HULL library chart to a Helm chart

If you do not have a Helm chart to start with you can make a copy of the [_hull-test_ Helm chart](./../files/test/HULL/sources/charts/hull-test) which is used for unit testing. You then need to rename the chart folder to your desired Helm chart's name and adjust the `Chart.yaml` to your desired charts name. 

To add the HULL library chart to an exsting Helm chart:

- choose a version that fits your targeted Kubernetes API versions best. The HULL chart version matches the implemented Kubernetes API version that is used for validation, so it should be at least the minimum version of the cluster(s) you target.

- follow the basic instructions on [how to add library charts to a Helm chart](https://helm.sh/docs/topics/library_charts/) to add HULL as a library chart to your Helm chart. 

  You can either download the chosen HULL chart from [the HULL releases page](https://github.com/vidispine/hull/releases) or add the public HULL repo to your Helm repos via this command:

      helm repo add hull https://vidispine.github.io/hull
      
  and pull it to use it locally. Otherwise just get it via the `dependencies` in the `Chart.yaml`
  
- from the HULL library chart you included, you need to copy the file named `hull.yaml` from the HULL charts root folder to your parent charts `/templates` folder. 

  ⚠️**This is required to have the HULL library functions render the objects specified under the key `hull.objects` in the parent chart! As of this moment Helm only considers files in the parent charts `/templates` folder for rendering. Consider adding this step to your build pipeline when creating releases of your Helm chart which include HULL.**⚠️

If these preliminary steps have been taken you can start using the HULL chart to render Kubernetes objects from your Helm chart.

---
Back to [README.md](./../README.md)
