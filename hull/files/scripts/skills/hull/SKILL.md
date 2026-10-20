---
name: hull
description: Write, convert, check and fix Helm charts built with the HULL library (vidispine/hull), whose Kubernetes objects are defined as values under hull.objects instead of templates. Use when a chart depends on hull, when values contain hull.objects or _HT transformations, when a HULL rendering error ("HULL failed with error [CODE]") needs fixing, or when converting an existing Helm chart or Kubernetes manifests to HULL.
---

# Working with HULL charts

A HULL chart has a single template, `templates/hull.yaml`, and defines every Kubernetes object as data in `values.yaml` under `hull.objects.<type>.<key>`. The values are validated by the JSON schema of the chart's HULL dependency. Do not write Go templates for objects.

## Workflow

Use the `hull` MCP tools when they are available:

1. Before writing values, read the rules once: `hull_docs` with topic `guide`.
2. Look up what is allowed instead of guessing: `hull_schema` with a values path such as `hull.objects.deployment.web.pod.containers.main`, an object type or a definition name.
3. After every change run `hull_validate` on the chart and fix every reported problem. Each problem is one line: `HULL failed with error [CODE] (@Values.<path>) <message> Fix: <hint>`. For details about a code use `hull_docs` with the code as topic.
4. Inspect the result with `hull_render`, using `kind` and `name` to select objects.
5. To convert an existing chart, render it with `helm template <release> <chart> --namespace <ns>` and pass the output to `hull_import` with the same release name and namespace. It writes a HULL chart and verifies that it renders the same objects. Then refactor the verified values into idiomatic HULL in small steps and compare the rendering after each step.

Without the MCP tools, the same is available as scripts in the HULL chart, in `files/scripts` of the dependency (unpack it with `tar -xzf charts/hull-*.tgz -C /tmp`): `python3 hull_validate.py <chart>`, `python3 hull_import.py --chart <dir> --verify <manifests>`, and the documentation in `files/doc`, starting with `agents.md`.

## Rules that differ from Kubernetes YAML

- The instance key is the name: `hull.objects.deployment.web` renders `<release>-<chart>-web`. `staticName: true` or `hull.config.general.noObjectNamePrefixes: true` keep the key unchanged.
- Write the fields of `spec` directly below the instance key, without `spec:`. Pod based objects take the pod spec in `pod`, CronJobs in `job.pod`. Pod labels and annotations go to `pod.labels` and `pod.annotations`.
- Named arrays are dictionaries keyed by name: `containers`, `initContainers`, `volumes`, `env`, `ports`. Never add `name:` to them. `volumeMounts`, `envFrom`, Ingress `rules`, `paths`, `tls` and `webhooks` are dictionaries with free keys. Elements render in key order, use an integer `order` property where order matters.
- Images: `image: {registry, repository, tag, digest}`; a non-empty digest replaces the tag. Quote tags like `"1.10"`.
- Selectors are generated from chart, release and key. A Service without `selector` selects the pods of the workload with the same key. An explicit `selector` keeps an existing selector; the pod labels must then match it.
- References to chart objects use the key and get the name prefix: configMap/secret/PVC volumes, env and envFrom refs, Ingress backends and TLS secrets, HPA targets. Add `staticName: true` next to a name that refers to an object outside the chart. `serviceAccountName`, `imagePullSecrets` and RoleBinding names are rendered as written; use `_HT^<key>` for the full name of a chart object.
- ConfigMap and Secret data: `data.<key>.inline` or `data.<key>.path`. Secret values are plain text, HULL encodes them. Add `noTemplating: true` to content containing `{{`.
- Defaults: `_HULL_OBJECT_TYPE_DEFAULT_` instances or elements, and named `sources`.
- The `default` ServiceAccount, Role and RoleBinding only exist with `hull.config.general.createDefaultRbacTriplet: true`.
- Kinds without a HULL object type are `generic` objects with `apiVersion`, `kind` and their fields.

## Transformations

Strings starting with these prefixes are computed:

| Prefix | Result |
| ------ | ------ |
| `_HT*hull.config.specific.x` | the value at the path below `.Values` |
| `_HT**Release.Name` | the same from the root context |
| `_HT!{{ ... }}` | a Go template result; `(index . "$")` is the root context |
| `_HT?<condition>` | a boolean, for `enabled` |
| `_HT^<key>` | the full name of a chart object |
| `_HT&<key>` | the generated selector labels of a key |

Keep shared values in `hull.config.specific` and reference them with `_HT*`. Write lists and dictionaries returned by `_HT!` in flow style.
