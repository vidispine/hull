------------------
[1.24.6]
------------------
CHANGES:
- changed transformation notation for include for better readability

FIXES:
- fixed and improve include transformation

------------------
[1.24.5]
------------------
CHANGES:
- add new include transformation and short form to allow compact usage of includes with minimum typing in values.yaml. 

FIXES:
- quote versions in Chart.yaml (https://github.com/vidispine/hull/issues/169)

------------------
[1.24.4]
------------------
CHANGES:
- for ConfigMap and Secret data, inline specification now always has precedence over path specification to make sure that content can always be overwritten at configuration time if required
- add active property to allow selecting amongst multiple volume definitions if they exist, eg. if a volume is defaulting to an emptyDir and is to be made a persistentVolumeClaim, the value of the active property (if specified) declares the concrete volume to render, otherwise Kubernetes will not accept multiple volume type definitions for a volume.

------------------
[1.24.3]
------------------
CHANGES:
- remove required property for endpoints and selector in ServiceMonitors from schema to allow better defaulting

------------------
[1.24.2]
------------------
CHANGES:
- add debug option renderBrokenHullGetTransformationReferences which allows to render HULL charts containing broken Get transformation references with non existing keys. By rendering these transformations with an informative placeholder instead of failing the chart rendering the broken references can be traced and fixed more easily before finishing writing the chart
- allows to use placeholder � to escape dots within key names so GET references also work when dots are within key names

------------------
[1.24.1]
------------------
CHANGES:
- improve intro documentation and add KH quote
- add Helm 3.9.0 to tests
- add option noObjectNamePrefixes to remove all object name prefixes globally

------------------
[1.24.0]
------------------
CHANGES:
- initial K8S 1.24 release
- deprecating 1.22 release
- added option to include ConfigMap binaryData from external path

------------------
[1.23.4]
------------------
CHANGES:
- added new objects Namespace, EndpointSlice and LimitRange

- update documentation

FIXES:
- disabling RBAC did not prevent rendering of Roles and ClusterRoles

------------------
[1.23.3]
------------------
CHANGES:
- added transformation pattern to array fields from ServiceMonitor definition
- update documentation

FIXES:
- HULL rules must be dictionary for roles in values.yaml

------------------
[1.23.2]
------------------
CHANGES:
- get transformation can now return complex dictionaries and array types
- introduce selector transformation and _HT& shortcut

FIXES:
- use fixed name template lower-case 'release-name' for helm template command compatibility with Helm 3.8. Previous versions created upper case 'RELEASE-NAME' by default for Release.Name which is changed to lowercase 'release-name' with Helm 3.8

------------------
[1.23.1]
------------------
CHANGES:
- allow to choose between rendering to single file or multiple files per object type to potentially eliminate performance penalty due to having one file only
- add test environments for both single and multi file usage
- add two example values.yamls

FIXES:
- allow using 63 instead of 54 chars for a fullname and name override
- remove dots end of labels and names

------------------
[1.23.0]
------------------
CHANGES:
- initial K8S 1.23 release
- deprecating 1.20 release

------------------
[1.22.13]
------------------
FIXES:
- changed probe port schema to anyOf to avoid clash when using oneOf transformation or string

------------------
[1.22.12]
------------------
FIXES:
- allow mixed transform only when dictionary is returned from transformation and other keys exist besides transformation trigger

------------------
[1.22.11]
------------------
CHANGES:
- added tests for get transformation results
- make every object field subjectable to string transformations irrelevant of input type by large scale extension of JSON schema

FIXES:
- using a get transformation to poulate Configmap/Secret contents produced bad 
character sequences

------------------
[1.22.10]
------------------
CHANGES:
- added short forms for transformations
- documentation improved

------------------
[1.22.9]
------------------
CHANGES:
- fix enabled properties allowed on policyrules in roles, envfrom and tls in ingresses
- allow shorter form of (index . "$") to access parent context

------------------
[1.22.8]
------------------

CHANGES:
- add hull.util.transformation.bool transformation

- BREAKING! change fields for registry population to overwrite any explicit registry fields 

------------------
[1.22.7]
------------------

CHANGES:
- add CHANGELOG.md
- add ingressclass objects as main objects
- allow to specify rules in roles key-value based instead of as an array (array also supported)
- add unit tests for ClusterRole and ClusterRoleBindings

FIXES: 
- clusterrole and clusterrolebinding objects with enabled=false or nulled were rendering incorrectly as empty objects 
- cronjob pods must not have selector set

------------------
[1.22.6]
------------------
CHANGES: 
- allow enabled property on all key-value pair HULL objects
- allow to use string as input for enabled property in order to use HULL transformations on enabled properties