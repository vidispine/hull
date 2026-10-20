# HULL for AI agents

This page is the compact reference for writing, converting and fixing HULL based Helm charts, aimed at AI coding agents and at people who want the rules on one page. It states the rules that differ from plain Kubernetes YAML and the workflow that catches mistakes. The other documents go into detail; this page links to them where needed. For complete, tested examples of common tasks see the [cookbook](/hull/files/doc/cookbook.md).

## The mental model

- **A HULL chart is data.** Its only template is `templates/hull.yaml` with one line, `{{- include "hull.objects.prepare.all" (dict "HULL_ROOT_KEY" "hull" "ROOT_CONTEXT" $) }}`. All Kubernetes objects are defined in `values.yaml` under `hull.objects.<type>.<key>`. There are no Go templates to write.
- **Everything is validated.** `values.schema.json` of the HULL library contains the Kubernetes API of the HULL release's Kubernetes minor version plus HULL's own properties. `helm lint`, `helm template` and `helm install` reject invalid values before anything is rendered.
- **The key is the name.** An object instance under `hull.objects.deployment.frontend` renders as a Deployment named `<release>-<chart>-frontend`. `staticName: true` on the object, or `hull.config.general.noObjectNamePrefixes: true` for all objects, renders the key as the name unchanged.
- **HULL fills in what is derivable:** `apiVersion`, `kind`, `metadata.name`, `metadata.namespace`, standard labels, workload selectors and the matching pod labels, Service selectors.
- **Object properties are flat.** For objects with a `spec` (Deployment, Service, Ingress, PVC, ...) the fields of the `spec` are written directly below the object key, without `spec:`. For objects without `spec` (ConfigMap, ServiceAccount, Role, ...) the object's top-level fields are written there. Pod based objects take the pod spec in `pod`, CronJobs in `job.pod`.

```yaml
hull:
  objects:
    deployment:
      frontend:                    # Deployment <release>-<chart>-frontend
        replicas: 2                # spec.replicas
        pod:                       # spec.template
          containers:
            main:                  # container 'main'
              image:
                repository: nginx
                tag: "1.27"
              ports:
                http:              # port 'http'
                  containerPort: 8080
    service:
      frontend:                    # Service <release>-<chart>-frontend, selects the pods of deployment 'frontend'
        type: ClusterIP
        ports:
          http:
            port: 80
            targetPort: http
```

## The workflow: write, check, read the error, fix

Do not trust values that were not rendered. Run these after every change and fix what they report before continuing:

```sh
helm dependency update ./mychart                    # once, fetches the HULL library
helm lint --strict ./mychart                        # schema validation and HULL checks
helm template my-release ./mychart > rendered.yaml  # renders and runs all HULL error checks
```

`hull/files/scripts/hull_validate.py ./mychart` runs the schema check and the rendering in one step and reports schema problems in the same one-line format as HULL's errors, see [tools for AI agents](/hull/files/doc/agent_tools.md). Add `# yaml-language-server: $schema=https://raw.githubusercontent.com/vidispine/hull/release-1.<minor>/hull/values.schema.json` as first line of a values file to have editors validate it while typing.

For a refactoring that should not change the result, keep the rendering from before the change and compare it: `diff before.yaml rendered.yaml`.

HULL errors have one line per problem and always the same form, with a code that is explained together with its fix in [error codes](/hull/files/doc/error_codes.md):

```
HULL failed with error [MISSING-IMAGE-REPOSITORY] (@Values.hull.objects.deployment.frontend.pod.containers.main.image.repository) Field repository is missing. Fix: Add a 'repository' to the container's 'image', ...
```

The `(@Values.<path>)` part is the location to fix. Errors starting with `values don't meet the specifications of the schema(s)` come from the JSON schema instead. Because most fields also accept a transformation string, the schema reports alternatives (`anyOf`). Look for the deepest path in the output and the reason given for it.

## Rules that differ from Kubernetes YAML

1. **Named arrays are dictionaries.** `containers`, `initContainers`, `volumes`, `env`, `envFrom`, `ports` of containers and Services, `volumeMounts`, Ingress `rules`, `paths` and `tls`, Role `rules`, `webhooks` and the arrays of Gateway API objects are written as dictionaries. For `containers`, `initContainers`, `volumes`, `env` and `ports` the key becomes the `name`. For `volumeMounts` and `webhooks` the key is free and `name` stays a property. The keys of `envFrom` and Ingress `rules`, `paths` and `tls` are free. Role `rules` and the Gateway API arrays also accept plain arrays.
2. **Order follows the keys.** Elements are rendered sorted alphanumerically by key. Where order matters, for example for `initContainers`, set an integer `order` property: lower values come first, equal values are sorted by key. An `env` variable is always rendered after the variables of the same container it references with `$(NAME)`. See [ordering](/hull/files/doc/chart_design.md#ordering-of-array-elements).
3. **`enabled: false` removes** an object or a dictionary element from the output. `enabled` also accepts a transformation such as `_HT?`, see below.
4. **Images are structured:** `image: { registry, repository, tag, digest }`, rendered as `registry/repository:tag`. A non-empty `digest` replaces the tag: `registry/repository@digest`. `hull.config.general.globalImageRegistryServer` sets the registry of all images.
5. **Pod template metadata** goes into `pod.labels` and `pod.annotations` (`templateLabels` and `templateAnnotations` on the object are equivalent). The object's own `labels` and `annotations` are rendered on the pod template too. On the pod template, `pod.labels` and `pod.annotations` take precedence over them and over HULL's standard labels (`app.kubernetes.io/*`, `helm.sh/chart`).
6. **Selectors are generated.** Deployments, StatefulSets and DaemonSets get the selector `app.kubernetes.io/name: <chart>`, `app.kubernetes.io/instance: <release>`, `app.kubernetes.io/component: <key>`, and their pods get these labels. A Service without `selector` selects the pods of the workload with the same key, so give a Service the key of its Deployment. To keep an existing selector, set `selector` explicitly; HULL then adds no selector labels to the pods and the pod labels must match it. Object `labels` must not override the three selector labels, rendering fails with `SELECTOR-NOT-MATCHING-POD-LABELS` otherwise.
7. **References to other objects of the chart use the key.** These fields are rendered with the same name prefix as objects: `configMap.name`, `secret.secretName` and `persistentVolumeClaim.claimName` of volumes, `configMapKeyRef.name` and `secretKeyRef.name` in `env`, `configMapRef.name` and `secretRef.name` in `envFrom`, `backend.service.name` and `tls.secretName` of Ingresses and `scaleTargetRef.name` of HorizontalPodAutoscalers. To reference an object that is not part of the chart, set `staticName: true` next to the name. All other names, for example `serviceAccountName`, `imagePullSecrets` and the `roleRef` and `subjects` of RoleBindings, are rendered as written. Use `_HT^<key>` there to get the full name of a chart object.
8. **ConfigMap and Secret data** is written as `data.<key>.inline` with the content or `data.<key>.path` with a chart file. Secret content is plain text, HULL encodes it; set `preEncoded: true` for content that is already base64 encoded. Both `inline` and file content are processed as Go templates. Set `noTemplating: true` for content that contains `{{` and is not meant for Helm, such as Prometheus or Grafana templates.
9. **Defaults for many objects:** values under `_HULL_OBJECT_TYPE_DEFAULT_` of an object type apply to all its instances, and `_HULL_OBJECT_TYPE_DEFAULT_` inside a dictionary (for example `containers`) applies to all its elements. Named templates are combined with `sources`. See [chart design](/hull/files/doc/chart_design.md).
10. **The `default` ServiceAccount, Role and RoleBinding** are not created unless `hull.config.general.createDefaultRbacTriplet: true`. Create a dedicated ServiceAccount and set `pod.serviceAccountName: _HT^<key>`.
11. **Anything else is passed through.** Fields HULL does not handle specially are rendered as given. For kinds without a HULL object type, such as custom resources, use `generic` objects with `apiVersion`, `kind` and any other fields.

## Transformations

A string value starting with one of these prefixes is computed while rendering. Transformations are resolved before rendering, in three passes, so they may reference values that are themselves transformations. See [transformations](/hull/files/doc/transformations.md).

| Prefix | Result | Example |
| ------ | ------ | ------- |
| `_HT*<path>` | The value at a dot separated path below `.Values`, of any type | `tag: _HT*hull.config.specific.version` |
| `_HT**<path>` | The same, starting at the root context, for `Release`, `Chart` or other charts | `_HT**Release.Name` |
| `_HT!<template>` | The result of a Go template, parsed as YAML | `replicas: _HT!{{ (index . "$").Values.hull.config.specific.replicas \| int }}` |
| `_HT?<condition>` | A boolean, the condition is written without `{{ }}` | `enabled: _HT?(index . "$").Values.hull.config.specific.monitoring` |
| `_HT^<key>` | The full object name for an instance key | `serviceAccountName: _HT^backend` |
| `_HT&<key>` | The generated selector labels for an instance key, as a dictionary | `matchLabels: _HT&frontend` |
| `_HT/<define>[:ARG:value...]` | The output of a Helm `define` called with `include` | `_HT/hull.metadata.chartref` |

Things to know:

- Put shared values in `hull.config.specific`, which accepts any structure, and reference them with `_HT*`. This replaces the Helm pattern of templating values into templates.
- Inside `_HT!`, `(index . "$")` is the chart's root context, so `(index . "$").Values` and `(index . "$").Release` are available. `(index . "OBJECT_INSTANCE_KEY")` and `(index . "OBJECT_TYPE")` refer to the current object. An `_HT*` reference can be embedded in an `_HT!` template.
- Write lists and dictionaries returned by `_HT!` in YAML flow style, for example `_HT![ "a", "b" ]`. A literal comma in an unquoted flow style item starts a new item. An `_HT*` reference embedded in `_HT!` belongs inside `{{ }}`: `_HT![ {{ _HT*hull.config.specific.host }} ]`.
- Transformations are not applied to single elements of a list. If the first element of a list is a transformation, its result replaces the whole list; other elements stay as written. To build a list from values use `_HT![ ... ]`, to use a whole list from the values reference it with `_HT*`.
- In an `_HT*` path, write a dot that belongs to a key as `§`: `_HT*hull.config.specific.example§com`. `§OBJECT_TYPE§` and `§OBJECT_INSTANCE_KEY§` are replaced by the current object's type and key.
- A reference to a path that does not exist fails with `HULL-GET-TRANSFORMATION-REFERENCE-INVALID`.
- Any string value that starts with one of the prefixes is treated as a transformation, also in imported content.

## Tools for agents

The Claude Code plugin of this repository (`/plugin install hull --marketplace vidispine/hull`) adds a skill with these rules and an MCP server with the tools `hull_docs`, `hull_schema`, `hull_validate`, `hull_render` and `hull_import`. The MCP server also works with other MCP clients. See [tools for AI agents](/hull/files/doc/agent_tools.md).

## Converting existing charts

`hull/files/scripts/hull_import.py` converts the output of `helm template` or other Kubernetes manifests into HULL values and verifies that the result renders the same objects:

```sh
helm template my-release ./old-chart --namespace ns > manifests.yaml
python3 hull/files/scripts/hull_import.py --chart ./new-chart --verify --release-name my-release --namespace ns manifests.yaml
```

Start every migration with it instead of converting by hand: the mechanical part is exact and verified, and the report lists every decision and every difference. Then refactor the verified result into idiomatic HULL in small steps, comparing the rendering after each step. See [importing charts](/hull/files/doc/import.md).

## Mapping Kubernetes kinds

| Kind | HULL object type | What goes below the instance key |
| ---- | ---------------- | -------------------------------- |
| Deployment, StatefulSet, DaemonSet, Job | `deployment`, `statefulset`, `daemonset`, `job` | `spec` fields, pod spec in `pod`, optional `selector` |
| CronJob | `cronjob` | `spec` fields, the job template's `spec` fields in `job`, pod spec in `job.pod` |
| Service | `service` | `spec` fields, `ports` as dictionary |
| Ingress | `ingress` | `spec` fields, `rules`, `rules.<key>.http.paths` and `tls` as dictionaries |
| ConfigMap, Secret | `configmap`, `secret` | `data.<key>.inline` or `.path`, other fields such as `type` |
| ServiceAccount, Namespace, StorageClass, PriorityClass | `serviceaccount`, `namespace`, `storageclass`, `priorityclass` | the object's top-level fields |
| Role, ClusterRole, RoleBinding, ClusterRoleBinding | `role`, `clusterrole`, `rolebinding`, `clusterrolebinding` | the object's top-level fields, Role `rules` as array or dictionary |
| PersistentVolumeClaim, PersistentVolume, HorizontalPodAutoscaler, PodDisruptionBudget, NetworkPolicy, ResourceQuota, LimitRange, IngressClass | lowercase kind | `spec` fields |
| Mutating- and ValidatingWebhookConfiguration | lowercase kind | `webhooks` as dictionary |
| Gateway API, admission policies, EndpointSlice, Endpoints, ServiceMonitor | lowercase kind | `spec` fields, or top-level fields for EndpointSlice and Endpoints |
| Docker registry credentials | `registry` | `server`, `username`, `password`; the secret is added to the `imagePullSecrets` of all pods that set none themselves |
| anything else | `generic` (or `customresource` if it has a `spec`) | `apiVersion`, `kind` and all other fields as given |

Every object also accepts `enabled`, `labels`, `annotations`, `staticName`, `metadataNameOverride`, `namespaceOverride`, `sources` and `conditionals`, see [object base](/hull/files/doc/API/hull_objects_base.md).

## Looking things up in the schema

`values.schema.json` is large. Query it instead of reading it, for example with `jq` in the HULL chart directory:

```sh
# all object types
jq -r '.definitions.root.properties.objects.properties | keys[]' values.schema.json
# the definition an object type uses, here deployment.v1
jq -r '.definitions.root.properties.objects.properties.deployment.patternProperties["^[^_].*$"].anyOf[1]["$ref"]' values.schema.json
# the HULL properties of a container and the HULL global settings
jq '.definitions["hull.Container.v1"].properties | keys' values.schema.json
jq '.definitions.root.properties.config.properties.general.properties | keys' values.schema.json
# the spec fields accepted directly below a Deployment instance
jq '.definitions["io.k8s.api.apps.v1.DeploymentSpec.Names"].enum' values.schema.json
```

The HULL specific properties of each object type are described in the [API documentation](/hull/files/doc/API/hull_objects_.md), the global settings in [hull.config](/hull/files/doc/API/hull_config.md).

## Common mistakes

| Mistake | What happens | Correct |
| ------- | ------------ | ------- |
| `containers:` written as a list | schema error at `containers` | a dictionary keyed by container name |
| `spec:` below a Deployment instance | schema error, `spec` is not a property | the `spec` fields directly below the instance key |
| `name:` given for a container, env variable or port | schema error `Property name of "name" does not match` | the key is the name |
| `serviceAccountName: backend` for a chart ServiceAccount `backend` | references a ServiceAccount literally named `backend` | `serviceAccountName: _HT^backend` |
| a Service key that differs from its Deployment's key without `selector` | the Service selects no pods | same key, or an explicit `selector` |
| `initContainers` relying on list order | they run in key order | `order` properties |
| Secret `data` values base64 encoded | encoded twice | plain text, or `preEncoded: true` |
| content with `{{ }}` in ConfigMap data | Helm processes it as a template and fails or changes it | `noTemplating: true` |
| `tag: 1.10` without quotes | the YAML number 1.1 renders as tag `1.1` | `tag: "1.10"` |
| `hosts: [_HT*hull.config.specific.host]` | the list is replaced by the string, Kubernetes rejects it | `hosts: _HT![ {{ _HT*hull.config.specific.host }} ]` |
| `args: [run, _HT*hull.config.specific.flag]` | the second element is not transformed | `args: _HT![ "run", {{ _HT*hull.config.specific.flag \| quote }} ]` |

---
Back to [README.md](/README.md)
