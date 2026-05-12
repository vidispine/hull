# Changelog

## [1.36.0]

CHANGES:

- initial K8S 1.36 release
- deprecating 1.33 release
- added new Kubernetes API objects that graduated to stable: `mutatingadmissionpolicy`, `mutatingadmissionpolicybinding`, `validatingadmissionpolicy` and `validatingadmissionpolicybinding`.
- added a new `generic` API object that allows to define generic objects of any sort. While `customresource` objects by definition need to have a `spec` field, this is not the case for `generic` objects, they only need a `kind` and an `apiVersion`. The idea is to offer an escape hatch for creating arbitrary and more exotic objects within the scope of HULL.

FIXES:

- fixed error when using function `hull.object.container.image` outside the scope of an object specification. In this case, missing logging parameters that are autopopulated in the scope of an object definition caused an error. The parameters are now populated with default values to prevent crashes.
