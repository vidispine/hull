# Adding the HULL library chart to a Helm chart

## The fast way

The by far easiest way to get started with HULL is to download the latest `hull-demo` release from the Releases page. It contains everything to directly start using HULL.

## The manual way

To manually add the HULL library chart to an existing Helm chart:

- choose a version that fits your targeted Kubernetes API versions best. The HULL chart version matches the implemented Kubernetes API version that is used for validation, so it should be at least the minimum version of the cluster(s) you target.

- follow the basic instructions on [how to add library charts to a Helm chart](https://helm.sh/docs/topics/library_charts/) to add HULL as a library chart to your Helm chart.

  You can either download the chosen HULL chart from [the HULL releases page](https://github.com/vidispine/hull/releases) or add the public HULL repo to your Helm repos via this command:

      helm repo add hull https://vidispine.github.io/hull
      
  and pull it to use it locally. Otherwise just get it via the `dependencies` in the `Chart.yaml`
  
- from the HULL library chart you included, you need to
  - copy the single file named `hull.yaml` from the HULL charts root folder to your parent charts `/templates` folder.

    or

  - copy all the files from the folder `/files/templates` to your parent charts `/templates` folder.

  ⚠️ **Generally it is required to have the single `hull.yaml` or the individual files from `/files/templates` HULL library functions render the objects specified under the key `hull.objects` in the parent charts `/templates` folder! As of this moment Helm only considers files in the parent charts `/templates` folder for rendering. Consider adding this step to your build pipeline when creating releases of your Helm chart which include HULL.** ⚠️
  
  ⚠️ **There are indications that when a single file in the parent Helm charts `/templates` folder contains many objects to render this impacts performance negatively when run against a real Kubernetes cluster. The time it takes to `helm template`, `helm update` or `helm install ` appears to be significantly longer when using one instead of several files. The reason for this is unclear and the behavior looks unneeded and fixable in Helm, it should not matter for processing if objects are read from many or a single template. But right now this would require a fix in Helm itself which is currently out of scope. To workaround this problem (or if you anyway like to have multiple files per object type for rendering) you can alternatively select to use the multiple files per object type from `/files/templates` instead of `hull.yaml` from the HULL charts root folder for rendering!** ⚠️

If these preliminary steps have been taken you can start using the HULL chart to render Kubernetes objects from your Helm chart.

---
Back to [README.md](/README.md)
