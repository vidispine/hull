# History
------------------
[1.30.4]
------------------
FIXES:
- fixed unwanted fields being merged when using the `sources` feature. When adding multiple sources, the intermediate results were not only merged into the target object but were also added to the sources themselves permanently. If `_HULL_OBJECT_TYPE_DEFAULT_` is in the sources list, this could lead to unwanted fields merged back into object instances that did not have sources specified and only inherited from `_HULL_OBJECT_TYPE_DEFAULT_` implicitly.

------------------
[1.30.3]
------------------
FIXES:
- If HULL errors are detected during processing, the processing is not stopped immediately. Instead, all errors are collected and printed after all objects were processed, making it easier to fix multiple problems in one go.
- Multiple HULL errors in one fields value are detectable now and can be shown. Previously only one error per field value was supported.

CHANGES:
- allow combination of bool and include transformations using extended `_HT?/` prefix. Include functions in Helm can only return string values [details in this Helm issue](https://github.com/helm/helm/issues/11231) so it is not possible to set a boolean value via retrieving the result of an include function triggered by `_HT/` include. Using `_HT?/` this is possible now, when the include returns a literal `true` or `false` this is treated as a boolean value using this syntax. See the [transformation documentation](./doc/transformations.md) for a detailed explanation and examples.
- allow usage of `_HT*` get transformation path syntax within `_HT!` tpl functions and `_HT?` bool transformations to reference `values.yaml` fields. Opposed to a more implementation heavy extension of `_HT*` to add more flexibility, this solution combines full Go templating flexibility while retaining a concise way of referencing fields in the `values.yaml` via `_HT*` syntax. Additionally, in the case, where only one templating operation is required, the extended `_HT!*` prefix allows to omit the double curly brace wrapping for even more conciseness. To e.g. reference and lower case and trim a `.yaml` suffix of a `values.yaml` field, this expression may be used: `field: _HT!* _HT*hull.config.specific.source | lower | trimSuffix ".yaml"`
- due to the introduction of combined transformations with two characters after `_HT` (`_HT?/` and `_HT!*`), the syntax for `_HT**` with added serialization instructions has been changed too so that `_HT**toJson|hull.config.specific.abc` is the valid syntax now. The former legal form, `_HT*toJson|*hull.config.specific.abc`, is still usable but considered legacy from now on.

------------------
[1.30.2]
------------------
CHANGES:
- allow to force render an otherwise disabled object using `hull.object.base.xyz` include by setting FORCE_ENABLED to true. This opens up the possibility to define object instance templates in HULL which are not deployed by HULL itself (by setting `enabled: false`). Instead, the object template can be rendered to a ConfigMap as a full-fledged Kubernetes YAML object which for example can serve as an object template the underlying application creates instances from.

------------------
[1.30.1]
------------------
FIXES:
- fix default RoleBinding between default Role and default ServiceAccount. Since namespace was not set for the default ServiceAccount reference, the default RBAC RoleBinding did not apply to the default ServiceAccount as intended.

CHANGES:
- add possibility to access array items in `_HT*` via using the item index for arrays instead of a dictionary key for dictionaries in the dotted path. Accessing into multiple nested arrays is possible like for example `_HT*hull.config.specific.outer-list.0.inner-list.1.key`. Related feature issue is [this one](https://github.com/vidispine/hull/issues/306)
- improve debugging broken YAML errors by including all available info in the generated error message. The error message now contains the actual YAML error and the reference to the specific object type and instance which could not be rendered.
- started adding reusable helper functions for use with `_HT/` in `_util_tools.tpl`. Populating the `data` for a Secret or ConfigMap with external files matching a GLOB pattern can be achieved by using `hull.util.tools.virtualdata.data.glob`. With `hull.util.tools.file.get`, the contents of an external file can be loaded conveniently outside of the ConfigMap and Secret `data` context. Thanks [ievgenii-shepeliuk](https://github.com/ievgenii-shepeliuk) for the ideas [in this isue](https://github.com/vidispine/hull/issues/311) 

------------------
[1.30.0]
------------------
CHANGES:
- initial K8S 1.30 release
- deprecating 1.27 release

------------------
[1.29.7]
------------------
CHANGES:
- added possibility to get values from the charts root with notation `_HT**`

------------------
[1.29.6]
------------------
CHANGES:
- added possibility to access the current object instance key and object type in `_HT*` transformations by using special keys `§OBJECT_INSTANCE_KEY§` and `§OBJECT_TYPE§` in the dotted path

------------------
[1.29.5]
------------------
FIXES:
- fixed `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` not existing in context of `_HT?` boolean transformations. Access to `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` is now provided same as in context of `_HT!` and `_HT/` transformations
- fixed inability to use `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` for `_HULL_OBJECT_TYPE_DEFAULT_` instances in context of `_HT/` include transformations. This fix allows to combine `postRender` replacements in content created by `_HT/` transformations on a `_HULL_OBJECT_TYPE_DEFAULT_` instance

------------------
[1.29.4]
------------------
FIXES:
- fixed problem with running both HULL transformations and `tpl` on `path` content in ConfigMaps and Secrets. After loading the external files content, decide whether to run HULL transformations or `tpl` based on HULL transformation prefix presence
- fixed checks for `virtualFolderDataPathExists` and `virtualFolderDataInlineValid` in the case of Secrets. Due to the Base64 encoding of data any error signaling strings weren't properly detected. With added Base64 decoding of the content for secrets the error checks now work for both ConfigMaps and Secrets
- make all keys within `.Values` available for reference in Secret and ConfigMap `data` `inline` and `path` content templating. Due to obsolete code, all other keys than `hull` were removed from the parent charts `.Values` context when being passed to ConfigMap and Secret for template processing. Thanks again [khmarochos](https://github.com/khmarochos) for pointing out the problem [in this isue](https://github.com/vidispine/hull/issues/288)

------------------
[1.29.3]
------------------
CHANGES:
- avoid rendering of empty collections. All `annotations`, `labels` and several other fields, which are explicitly handled by HULL, now are fully omitted if they resolve to empty dictionaries or arrays. This changed behaviour can be reverted by individually choosing to render `emptyAnnotations`, `emptyLabels`, `emptyTemplateAnnotations`, `emptyTemplateLabels` and/or `emptyHullObjects` under `config.global.render`. This default behavior change is in favor of improving compatibility with tools that potentially auto-prune empty collection fields like ArgoCD and thus may have syncing issues with empty collections. In terms of severity this change is considered non-breaking. Down the line, Kubernetes treats missing and empty collection fields in the same way. Note that per the schema, some collection fields are required (`containers` in `pod` and `paths` in `ingress` `rules`) and omitting them or leaving them empty now violates the Kubernetes schema. However, in these cases Kubernetes also verifies that at least one element is in the collection on deployment so the problem only shows earlier. Thanks [alexrimlin](https://github.com/alexrimlin) for the suggestion!

------------------
[1.29.2]
------------------
CHANGES:
- removed hardcoded `type: Opaque` and allow to freely set type of Secrets, thanks [khmarochos](https://github.com/khmarochos) for [PR](https://github.com/vidispine/hull/pull/275)
- enabled specification of `configmap` and `secret` `data` inline` fields as dictionaries or lists and added implicit and explicit serialization to `configmap` and `secret` `data` entries. Implicit and automatic serialization takes place for files ending with `.json` (`toPrettyJson`) and files ending with `.yaml` and `.yml` (`toYaml`) if the `inline` content is a dictionary or a list. Explicit serialization is possible using the new `serialization` property for `data` elements and can be applied to dictionary, list and string `inline` entries and string `path` contents. Thanks [khmarochos](https://github.com/khmarochos) for the idea [in this report](https://github.com/vidispine/hull/issues/267)
- added optional serialization arguments to `_HT/` and `_HT*` to serialize dictioanry and lists `toJson`, `toPrettyJson`, `toRawJson`, `toString` or `toYaml`, also thanks [khmarochos](https://github.com/khmarochos) for the idea [in this report](https://github.com/vidispine/hull/issues/267)
- added optional `postRender` option to inject object instance key or object name strings into rendered object YAML. This enables very efficient specification of multiple identical object instances via the `sources` and `_HULL_OBJECT_TYPE_DEFAULT_` feature and last-minute insertion of the actual object instance key or name into the rendered YAML string. Handle with caution since this can invalidate the YAML structure!
- added error checks in HULL to prevent common configuration errors by failing the Helm command. By default verify `image` specifications exist and are valid for all `containers`, files pointed to via `path` physically exist and all tree elements in a `_HT*` references are resolvable

FIXES:
- fixed hashsumAnnotation calculation of secrets incorrectly being done on Base64 encoded value instead of decoded value
- centralized `configmap` and `secret` functionality and tests to guarantee exact same handling whether content is defined `inline` or in a file with `path`. Code difference between `secret` and `configmap` reduced to only late base64 value encoding in the case of secrets.
- improve code in helper functions, thanks [JuryA](https://github.com/JuryA) for [PR](https://github.com/vidispine/hull/pull/277)

------------------
[1.29.1]
------------------
CHANGES:
- removed all required field definitions from values.schema.json. Validating required fields is helpful on the output side because it indicates which fields are important in the rendered output but on input side side they block the full potential of efficient defaulting. When present, The JSON schema demands that required fields are added to all individual instances of an object - even when a source or _HULL_OBJECT_TYPE_DEFAULT_ has already set them appropriately and concisely. This leads often to unnecessary bloat and complexity in the values.yaml and therefore the usage of required fields in the JSON schema was dropped favor of cleaner chart design. 
- added tests to solidify expectations on workarounds for YAML parser issues with large numbers (unwanted rendering in scientific notation, unwanted interpretation of strings as scientific notation). The issues mentioned [in this report](https://github.com/vidispine/hull/issues/262) cannot be solved in HULL but the tests should from now on indicate if something has changed in Helm about the applicability of the workarounds, thanks [seniorquico](https://github.com/seniorquico)

FIXES:
- fixed bug where imagePullSecrets cannot be overwritten with empty list, thanks [khmarochos](https://github.com/khmarochos)

------------------
[1.29.0]
------------------
CHANGES:
- initial K8S 1.29 release
- deprecating 1.26 release

------------------
[1.28.6]
------------------
FIXES:
- fix still broken CronJob rendering which is now in line with the rendering style of other object types 

------------------
[1.28.5]
------------------
FIXES:
- fix broken _HULL_OBJECT_TYPE_DEFAULT_ defaulting of CronJobs properties where all values from _HULL_OBJECT_TYPE_DEFAULT_ or sources where not merged to rendered CronJob instances
- fix missing rendering of embedded Job Kubernetes properties in a Cronjobs jobTemplate where any Kubernetes property of an embedded Job was missing from the rendered output

------------------
[1.28.4]
------------------
FIXES:
- fix sources feature not properly working for non-pod based object types
- fix OBJECT_INSTANCE_KEY handling causes error for calls to hull.util.transformation.tpl originating outside of hull.util.transformation

------------------
[1.28.3]
------------------
CHANGES:
- introducing more flexible mechanism to populate default values for object intances. It is possible to opt to load default values from zero to multiple object instances by using new hull.base.v1 property sources. All referenced object instances are merged in the provided order to allow sharing definitions between object instances and object types. The default behavior to merge default values from _HULL_OBJECT_TYPE_DEFAULT_ remains intact.

FIXES:
- added icon to Chart.yaml to fix linter warning
- fail with speaking error message instead of hard to decode error message when path elements in get transformations are not found

------------------
[1.28.2]
------------------
FIXES:
- extend loosening of schema type to env fields. User input of type float, integer or boolean is now allowed and on rendering a late to string conversion is taking place to guarantee the Kubernetes schema is not violated demanding string values. 

------------------
[1.28.1]
------------------
FIXES:
- loosen schema types of image tag, annotation and label values. For image tag values user input of type float or integer and for annotation and label values user input of type float, integer and boolean is allowed. On rendering a late to string conversion is taking place to guarantee the Kubernetes schema is not violated demanding string values. Reasoning behind is that for these fields correct quoting of user input is often missing in case of values which are interpreted as non-strings. Allowing a flexible input type and late guaranteed conversion to string helps avoid unncessary and unexpected errors due to user input.
- drop kubeVersion from Chart.yaml to support running hull-demo in lower version clusters, kubeVersion field does not seem to have relevance for hull as a library chart but is copied over to hull-demo Chart.yaml

------------------
[1.28.0]
------------------
CHANGES:
- initial K8S 1.28 release
- deprecating 1.25 release
- allow to use implicitly set OBJECT_INSTANCE_KEY and OBJECT_TYPE context variables for accessing an object instance's key and type as strings in the context of transformations executed within an object instance's specification.

------------------
[1.27.1]
------------------
CHANGES:
- allow to set an explicit namespaceOverride via chart configuration on the object instances rendered. This is helpful for usage with helm template command so that rendered templates contain a namespace and can be used directly in GitOps style declarative workflows. If no namespaceOverride is provided, the namespace is now still always added to the object instances and falls back to the release namespace.

------------------
[1.27.0]
------------------
CHANGES:
- initial K8S 1.27 release
- deprecating 1.24 release

------------------
[1.26.2]
------------------
CHANGES:
- by adding property hashsumAnnotation: true to a pods volumeMount, env or envFrom referencing a ConfigMap or Secret, a pod restart can be enforced in case of changed contents. This works by calculation of a hashsum of the contents and adding it to the pods template annotations. This is recommended practice as documented in the [Helm documentation](https://helm.sh/docs/howto/charts_tips_and_tricks/#automatically-roll-deployments) in order to handle applications that require restarts on certain configuration changes.

------------------
[1.26.1]
------------------
CHANGES:
- add metadataNameOverride possibility to Hull.Object.Base to allow setting an object instance metadata.name that is different from the implicit component key. This enables special use-cases where e.g. the definition of a custom resource instance is done in the chart's values.yaml under a fixed key and the CustomResources actual instance name - maybe playing an important role for the operator functionality - is only set at deployment time dynamically

------------------
[1.26.0]
------------------
CHANGES:
- initial K8S 1.26 release
- deprecating 1.23 release
- build and release hull-demo chart for easy demoing and bootstrapping HULL based Helm Charts

FIXES:
- improved schema structure for centrally defined probe configurations ([PR](https://github.com/vidispine/hull/pull/202), thanks [matthias4217](https://github.com/matthias4217))
- fix merging order for tests with additional overlay values.yamls

------------------
[1.25.10]
------------------
FIXES:
- when a dictionary structure contains a _HULL_TRANSFORMATION_ key for producing dynamically rendered key-value content and additional static keys side-by-side, transformations were not being correctly processed for the structures beneath the static key contents
- some minor documentation fixes (links in main README.md, broken structures)

------------------
[1.25.9]
------------------
FIXES:
- fixed incorrect schema structure for imagePullPolicy enums (thanks [matthias4217](https://github.com/matthias4217))

------------------
[1.25.8]
------------------
FIXES:
- fixed general linter error due to bad whitespace chomping between YAML objects, this did not affect template rendering however (https://github.com/vidispine/hull/issues/186)
- added strict linting to test cases, now all cases must not emit linting WARNINGs or ERRORs to be considered successful

------------------
[1.25.7]
------------------
FIXES:
- extend transformation scope from objects spec to Values.hull when computing initial transformations, fixes cases with first transformation resolving to another transformation which is then not resolved itself
- speed up rendering by only run transformations once on complete Values.hull dictionary instead of running it once for each object type

------------------
[1.25.6]
------------------
FIXES:
- render emtpy string instead of <nil> when ConfigMap or Secret inline input is nil pointer

CHANGES:
- add debug option renderNilWhenInlineIsNil to print out <nil> instead of empty string when an inline value resolves to a nil pointer
- add debug option renderPathMissingWhenPathIsNonExistent to print out information about a missing file for a path value instead of an empty string when a path value does not resolve to an actual file

------------------
[1.25.5]
------------------
CHANGES:
- changed transformation notation for include for better readability

FIXES:
- fixed and improve include transformation

------------------
[1.25.4]
------------------
CHANGES:
- add new include transformation and short form to allow compact usage of includes with minimum typing in values.yaml. 

FIXES:
- quote versions in Chart.yaml (https://github.com/vidispine/hull/issues/169)

------------------
[1.25.3]
------------------
CHANGES:
- for ConfigMap and Secret data, inline specification now always has precedence over path specification to make sure that content can always be overwritten at configuration time if required
- add active property to allow selecting amongst multiple volume definitions if they exist, eg. if a volume is defaulting to an emptyDir and is to be made a persistentVolumeClaim, the value of the active property (if specified) declares the concrete volume to render, otherwise Kubernetes will not accept multiple volume type definitions for a volume.

------------------
[1.25.2]
------------------
CHANGES:
- remove required property for endpoints and selector in ServiceMonitors from schema to allow better defaulting

------------------
[1.25.1]
------------------
CHANGES:
- add debug option renderBrokenHullGetTransformationReferences which allows to render HULL charts containing broken Get transformation references with non existing keys. By rendering these transformations with an informative placeholder instead of failing the chart rendering the broken references can be traced and fixed more easily before finishing writing the chart
- allows to use placeholder § to escape dots within key names so GET references also work when dots are within key names

------------------
[1.25.0]
------------------
CHANGES:
- initial K8S 1.25 release
- deprecating 1.22 release
- removed PodSecurityPolicy

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
- deprecating 1.21 release
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