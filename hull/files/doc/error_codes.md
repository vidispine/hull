# Error codes

When HULL detects a problem while rendering, `helm template`, `helm install` and `helm upgrade` fail and print one line per problem, followed by a line pointing to this page:

```
Error: execution error at (mychart/templates/hull.yaml:1:4):
HULL failed with error [MISSING-IMAGE-REPOSITORY] (@Values.hull.objects.deployment.frontend.pod.containers.main.image.repository) Field repository is missing. Fix: Add a 'repository' to the container's 'image', for example 'repository: nginx'. The 'registry', 'tag' and 'digest' are optional.
All HULL error codes and how to fix them are explained in https://github.com/vidispine/hull/blob/main/hull/files/doc/error_codes.md
```

Every error line has the same structure, so it can be read by people and processed by scripts and AI agents alike:

```
HULL failed with error [<CODE>] (@Values.<path>) <message> Fix: <how to fix it>
```

| Part | Meaning |
| ---- | ------- |
| `<CODE>` | A stable identifier of the kind of error. Codes are not renamed between releases, so it is safe to match on them. Each code has a section below. |
| `(@Values.<path>)` | Where the problem is, as a path into the chart's values. For errors in transformations it is the place where the transformation is used. |
| `<message>` | What exactly is wrong, including the offending value where that helps. |
| `Fix:` | The usual way to resolve this kind of error. |

A regular expression matching an error line is `^HULL failed with error \[([A-Z0-9-]+)\] \(@([^)]*)\) (.*?)(?: Fix: (.*))?$`.

Some things to know about how errors are reported:

- Errors of all objects are collected and reported together, so a single run shows every problem. The `MISSING-SOURCE-*` errors are the exception: they stop rendering immediately because the object cannot be assembled without its sources.
- Errors are only reported for objects that are rendered. A problem in a disabled object or a disabled container does not fail the chart.
- If the same problem shows up more than once in an object, for example in the object's and the pod's metadata, it is reported once.
- Some checks can be switched off or on with the `hull.config.general.errorChecks` settings, see [error checking](/hull/files/doc/error_checking.md). The table below lists which setting controls which code.

> Errors that start with `values don't meet the specifications of the schema(s)` are not HULL errors. They come from Helm validating the values against HULL's [JSON schema](/hull/files/doc/json_schema_validation.md) before HULL runs. Most fields also accept a transformation string, so the schema reports a failure as a set of alternatives (`anyOf`). Look for the deepest path in the output and the reason given for it, such as a pattern that does not match or a wrong type. Or run [`hull_validate.py`](#checking-a-chart-with-hull_validatepy), which reports each schema problem on one line in the format above, with the codes listed under [schema problems](#schema-problems).

## Overview

| Code | Raised when | Controlled by |
| ---- | ----------- | ------------- |
| [`MISSING-IMAGE-SPEC`](#missing-image-spec) | A container has no `image` | `errorChecks.containerImageValid` |
| [`MISSING-IMAGE-REPOSITORY`](#missing-image-repository) | A container's `image` has no `repository` | `errorChecks.containerImageValid` |
| [`INVALID-IMAGE-DIGEST`](#invalid-image-digest) | A container's `image.digest` is not a valid digest | `errorChecks.containerImageValid` |
| [`MISSING-CRONJOB-JOB`](#missing-cronjob-job) | A CronJob has no `job` | always checked |
| [`MISSING-NAMESPACE-OVERRIDE`](#missing-namespace-override) | `namespaceOverride` is set to an empty string | always checked |
| [`VIRTUAL-FOLDER-DATA-INLINE-INVALID`](#virtual-folder-data-inline-invalid) | A ConfigMap or Secret `data` entry has a null `inline` | `errorChecks.virtualFolderDataInlineValid` (off by default) |
| [`VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING`](#virtual-folder-data-path-not-existing) | A ConfigMap or Secret `data` entry's `path` matches no file | `errorChecks.virtualFolderDataPathExists` |
| [`HULL-GET-TRANSFORMATION-REFERENCE-INVALID`](#hull-get-transformation-reference-invalid) | An `_HT*` reference points to a key that does not exist | `errorChecks.hullGetTransformationReferenceValid` |
| [`BROKEN-OBJECT-YAML`](#broken-object-yaml) | The YAML rendered for an object cannot be parsed | `errorChecks.objectYamlValid` |
| [`SELECTOR-NOT-MATCHING-POD-LABELS`](#selector-not-matching-pod-labels) | A workload's `selector.matchLabels` are not all found in its pod template labels | always checked |
| [`DEFAULT-RBAC-OBJECT-NOT-RENDERED`](#default-rbac-object-not-rendered) | The `default` ServiceAccount, Role or RoleBinding is customized but not rendered | always checked |
| [`MISSING-SOURCE-TEMPLATE`](#missing-source-template) | A pod or container `sources` entry names an undefined template | always checked |
| [`MISSING-SOURCE-OBJECT-TYPE`](#missing-source-object-type) | An object `sources` entry names an object type that does not exist | always checked |
| [`MISSING-SOURCE-OBJECT-INSTANCE`](#missing-source-object-instance) | An object `sources` entry names an object instance that does not exist | always checked |

## Checking a chart with hull_validate.py

`hull/files/scripts/hull_validate.py` checks a chart in two steps and stops after the first one that finds problems. First it validates the values against the schema of the chart's HULL dependency, merged like Helm merges them, then it renders the chart with `helm template` and reports HULL's errors:

```sh
python3 hull/files/scripts/hull_validate.py ./mychart                 # values.yaml of the chart
python3 hull/files/scripts/hull_validate.py ./mychart -f prod.yaml    # plus additional values files
python3 hull/files/scripts/hull_validate.py --hull ./hull -f my.hull.yaml --no-render
python3 hull/files/scripts/hull_validate.py ./mychart --json          # machine readable
```

It needs Python 3.8 or newer with PyYAML and jsonschema (`pip install pyyaml jsonschema`), and `helm` for the rendering step. The exit code is `0` without problems, `1` with problems and `2` if the chart could not be read. Each problem is printed in the same format as HULL's errors, so both are handled alike:

```
HULL failed with error [SCHEMA-UNKNOWN-PROPERTY] (@Values.hull.objects.service.web.ports.http) Property 'protocl' is not allowed here, did you mean 'protocol'? Allowed are appProtocol, enabled, name, nodePort, order, port, protocol, targetPort. Fix: Remove the property or move it to where it belongs. The allowed properties are listed in the message.
```

## Codes

### `MISSING-IMAGE-SPEC`

A container or init container has no `image`. Kubernetes rejects pods with a container without image.

```
HULL failed with error [MISSING-IMAGE-SPEC] (@Values.hull.objects.deployment.frontend.pod.containers.main.image) Field image is missing.
```

**Fix:** add an `image` with at least a `repository`. If the image is supplied by other means, for example by a mutating admission webhook, set `hull.config.general.errorChecks.containerImageValid` to `false`.

```yaml
containers:
  main:
    image:
      repository: nginx
      tag: "1.27"
```

### `MISSING-IMAGE-REPOSITORY`

A container's `image` exists but has no `repository`, so no image name can be rendered.

```
HULL failed with error [MISSING-IMAGE-REPOSITORY] (@Values.hull.objects.deployment.frontend.pod.containers.main.image.repository) Field repository is missing.
```

**Fix:** add the `repository`. The `registry`, `tag` and `digest` are optional, see the [image specification](/hull/files/doc/API/hull_objects_pod.md#the-hullimagev1-properties).

### `INVALID-IMAGE-DIGEST`

A container's `image.digest` is set but is not an image digest. A digest is an algorithm and the hex encoded hash of the image joined by a colon, for example `sha256:1ff6c18fbef2045af6b9c16bf034cc421a29027b800e4f9b68ae9b1cb3e9ae07`. Literal values are already rejected by the JSON schema, this check catches digests that result from a transformation.

```
HULL failed with error [INVALID-IMAGE-DIGEST] (@Values.hull.objects.deployment.frontend.pod.containers.main.image.digest) Field digest '1a2b3c4d5e6f' is not a valid image digest.
```

**Fix:** use the complete digest, for example as printed by `docker buildx imagetools inspect <image>` or `crane digest <image>`. The 12 character image ID shown by `docker images` is not a digest. To pull by tag instead, remove `digest` or set it to an empty string.

### `MISSING-CRONJOB-JOB`

A CronJob has no `job`, neither in its own values nor from `_HULL_OBJECT_TYPE_DEFAULT_` or `sources`, so there is no job template to render.

```
HULL failed with error [MISSING-CRONJOB-JOB] (@Values.hull.objects.cronjob.cleanup.job) Field job is missing.
```

**Fix:** add `job` with the fields of the job template's `spec` and the pod in `job.pod`, see the [scheduled job recipe](/hull/files/doc/cookbook.md#scheduled-job).

### `MISSING-NAMESPACE-OVERRIDE`

An object's `namespaceOverride` is an empty string.

```
HULL failed with error [MISSING-NAMESPACE-OVERRIDE] (@Values.hull.objects.deployment.frontend.namespaceOverride) Field namespaceOverride cannot be empty.
```

**Fix:** set `namespaceOverride` to the namespace the object belongs to, or remove it so that the object is deployed to the release namespace. If the value comes from a transformation, check that the referenced value is set.

### `VIRTUAL-FOLDER-DATA-INLINE-INVALID`

A ConfigMap or Secret `data` entry has an `inline` that is `null`. This is only reported if `hull.config.general.errorChecks.virtualFolderDataInlineValid` is `true`, by default such entries render as empty strings.

```
HULL failed with error [VIRTUAL-FOLDER-DATA-INLINE-INVALID] (@Values.hull.objects.configmap.settings.data.app.conf.inline) Inline data is invalid.
```

**Fix:** give `inline` a value or remove the entry. A `null` usually comes from a values key without value or a transformation that resolved to nothing.

### `VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING`

A ConfigMap or Secret `data` entry has a `path` that does not match a file in the chart.

```
HULL failed with error [VIRTUAL-FOLDER-DATA-PATH-NOT-EXISTING] (@Values.hull.objects.configmap.settings.data.app.conf.path) Path files/app.conf does not exist.
```

**Fix:** make `path` point to a file inside the chart, relative to the chart root, such as `files/app.conf`. Files matched by `.helmignore` are not packaged and therefore not found. For literal content use `inline` instead of `path`.

### `HULL-GET-TRANSFORMATION-REFERENCE-INVALID`

An `_HT*` get transformation, also inside an `_HT!` template or a `conditionals` condition, references a key that does not exist.

```
HULL failed with error [HULL-GET-TRANSFORMATION-REFERENCE-INVALID] (@Values.hull.objects.deployment.frontend.pod.containers.main.image.tag) Element versoin in path hull.config.specific.versoin was not found.
```

**Fix:** correct the reference or add the missing key. A reference is a dot separated path relative to `.Values`, for example `_HT*hull.config.specific.version`. A dot that is part of a key is written as `§`, for example `_HT*hull.config.specific.domain§com`. See [transformations](/hull/files/doc/transformations.md).

### `BROKEN-OBJECT-YAML`

The YAML rendered for an object cannot be parsed. The message contains the YAML parser's error, with the line number inside the rendered object.

```
HULL failed with error [BROKEN-OBJECT-YAML] (@Values.hull.objects.deployment.frontend) The rendered object is not valid YAML, parsing it failed with 'error converting YAML to JSON: yaml: line 96: found character that cannot start any token'.
```

**Fix:** find the value that breaks the YAML. Typical causes are values that end up unquoted in the output and start with a YAML indicator character such as `@`, `` ` ``, `%` or `*`, for example an image without `repository` and only a `digest` while `containerImageValid` is off, and `_HT!` templates whose output has wrong indentation. `helm template --debug` prints the broken object.

### `SELECTOR-NOT-MATCHING-POD-LABELS`

The `selector.matchLabels` of a Deployment, StatefulSet, DaemonSet or Job are not all present with the same value in the labels of its pod template. Kubernetes rejects such an object, HULL reports it while rendering instead.

```
HULL failed with error [SELECTOR-NOT-MATCHING-POD-LABELS] (@Values.hull.objects.deployment.frontend) The selector does not select the pods of the pod template, selector label 'app.kubernetes.io/component: frontend' is 'app.kubernetes.io/component: web' in the pod template.
```

There are two typical causes:

- The object's `labels` set one of the labels of the generated selector (`app.kubernetes.io/name`, `app.kubernetes.io/instance` or `app.kubernetes.io/component`) to a different value. Object `labels` are also rendered on the pod template and take precedence there.
- An explicit `selector` was given, but the labels it selects are not set for the pods. With an explicit `selector`, HULL does not add its generated selector labels to the pod template.

**Fix:** remove the conflicting label from the object's `labels`, or with an explicit `selector` add the selected labels to `pod.labels`. See [pod templates](/hull/files/doc/API/hull_objects_pod.md#the-hullpodtemplatev1-properties).

### `DEFAULT-RBAC-OBJECT-NOT-RENDERED`

The `default` ServiceAccount, Role or RoleBinding was customized, but is not rendered because `hull.config.general.createDefaultRbacTriplet` is `false`. Without this error the customization would silently have no effect.

```
HULL failed with error [DEFAULT-RBAC-OBJECT-NOT-RENDERED] (@Values.hull.objects.role.default.rules) The 'default' Role has rules but is not rendered because 'hull.config.general.createDefaultRbacTriplet' is false.
```

**Fix:** set `hull.config.general.createDefaultRbacTriplet` to `true` to render all three default objects, or set `enabled` explicitly on the customized object to decide for it alone.

### `MISSING-SOURCE-TEMPLATE`

A pod or container `sources` entry names a template that is not defined under `hull.config.templates.pod` or `hull.config.templates.container`.

```
HULL failed with error [MISSING-SOURCE-TEMPLATE] (@Values.hull.objects.deployment.frontend.pod.sources) Source 'monitoring' is not defined in 'hull.config.templates.pod'.
```

**Fix:** define the template or remove its name from `sources`. See [chart design](/hull/files/doc/chart_design.md) on sharing configuration with `sources`.

### `MISSING-SOURCE-OBJECT-TYPE`

An object instance `sources` entry of the form `<instance>[<objecttype>]` names an object type that does not exist.

```
HULL failed with error [MISSING-SOURCE-OBJECT-TYPE] (@Values.hull.objects.deployment.frontend.sources) Object type 'deploymnet' of source 'base' does not exist in 'hull.objects'.
```

**Fix:** use an existing object type in lowercase, such as `base[deployment]`, or write the entry as `<instance>` to refer to an instance of the same object type.

### `MISSING-SOURCE-OBJECT-INSTANCE`

An object instance `sources` entry names an object instance that does not exist.

```
HULL failed with error [MISSING-SOURCE-OBJECT-INSTANCE] (@Values.hull.objects.deployment.frontend.sources) Source 'base' does not exist in 'hull.objects.deployment'.
```

**Fix:** add the referenced instance, typically as a disabled template instance with `enabled: false`, or remove it from `sources`. An entry without `[<objecttype>]` refers to an instance of the same object type as the object it is used in.

## Schema problems

These codes are reported by `hull_validate.py` for values that do not match the JSON schema. Helm reports the same problems, in its own format, as `values don't meet the specifications of the schema(s)`.

### `SCHEMA-UNKNOWN-PROPERTY`

A property is not allowed where it is used. The message lists the allowed properties and suggests the closest one.

```
HULL failed with error [SCHEMA-UNKNOWN-PROPERTY] (@Values.hull.objects.deployment.frontend) Property 'spec' is not allowed here. Allowed are annotations, conditionals, enabled, labels, ..., replicas, revisionHistoryLimit, selector, sources, staticName, strategy, templateAnnotations, templateLabels.
```

**Fix:** remove the property or move it. Typical cases have their own hint: the fields of `spec` are written directly below the object instance key, a dictionary key already is the `name`, and the pod template is written as `pod`.

### `SCHEMA-UNKNOWN-OBJECT-TYPE`

A key below `hull.objects` is not a HULL object type.

**Fix:** use one of the object types listed in the message, in lowercase. Kinds without an object type are created as `generic` objects.

### `SCHEMA-WRONG-TYPE`

A value has the wrong type, for example a string where an integer is expected, or a list where HULL expects a dictionary.

```
HULL failed with error [SCHEMA-WRONG-TYPE] (@Values.hull.objects.deployment.frontend.pod.containers) Expected a dictionary or a HULL transformation, got a list [{"name": "main", "image": "nginx"}].
```

**Fix:** give a value of the expected type. HULL writes named arrays like `containers`, `env`, `ports` or `volumes` as dictionaries keyed by name. Where the message says a HULL transformation is allowed, a string starting with `_HT` is accepted too.

### `SCHEMA-INVALID-VALUE`

A value has the right type but is not allowed, for example it does not match a pattern or is not one of the allowed values. The message shows the value and what is expected.

**Fix:** give an allowed value.

### `SCHEMA-MISSING-PROPERTY`

A required property is missing.

**Fix:** add the property named in the message.

---
Back to [README.md](/README.md)
