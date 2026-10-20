# Importing existing charts and manifests

`hull/files/scripts/hull_import.py` converts Kubernetes manifests into HULL values. Its main use is migrating an existing chart to HULL: render the old chart with `helm template`, convert the output, and let the tool prove that the new HULL chart renders the same objects.

The conversion is deterministic, so the same input always gives the same values, and it is checked: with `--verify` the converted chart is rendered with Helm and compared object by object with the input. A conversion that verifies can be trusted without reading it line by line, by people as well as by AI agents. The result is a correct starting point that still looks like the original chart; turning it into idiomatic HULL is a separate step described [below](#making-the-result-idiomatic).

## Requirements

- Python 3.8 or newer with PyYAML (`pip install pyyaml`)
- `helm` for `--verify`
- The HULL chart directory. When the script is run from a HULL checkout or an unpacked HULL chart it finds the chart itself, otherwise pass `--hull <path to the hull chart directory>`.

## Usage

Convert an existing chart, write a new HULL based chart and verify it:

```sh
helm template my-release ./old-chart --namespace my-namespace > manifests.yaml
python3 hull/files/scripts/hull_import.py --chart ./new-chart --verify \
  --release-name my-release --namespace my-namespace manifests.yaml
```

The written chart contains `Chart.yaml` with the HULL dependency, `templates/hull.yaml`, the converted `values.yaml` and a copy of the HULL library in `charts/hull` so that it renders offline. Run `helm dependency update` to replace the copy by the published HULL package.

Other ways to call it:

```sh
# only print the values
python3 hull_import.py manifests.yaml

# read from stdin, write values to a file, keep a machine readable report
helm template my-release ./old-chart | python3 hull_import.py -o values.yaml --report report.json -

# convert a directory of YAML files, for example kubectl get -o yaml exports
python3 hull_import.py --verify ./manifests/
```

| Option | Meaning |
| ------ | ------- |
| `-o`, `--output` | Write the values to this file instead of stdout. |
| `--chart` | Write a complete HULL based chart to this directory. |
| `--chart-name` | Name of the written chart, by default the directory name. |
| `--hull` | The HULL chart directory to use for the chart and for verification. |
| `--verify` | Render the converted chart with `helm template` and compare it with the input. |
| `--release-name` | The release name used for `--verify`. Use the one the input was rendered for. |
| `--namespace` | The namespace the input was rendered for. Objects in it get no `namespaceOverride`. |
| `--kube-version` | Passed to `helm template` as `--kube-version` when verifying. |
| `--helm` | The helm binary to use. |
| `--report` | Write the notes and the verification result as JSON to this file. |

The exit code is `0` if the conversion succeeded and, with `--verify`, all objects are identical, `1` if verification found differences and `2` if the input could not be read or the converted chart could not be rendered.

## What the conversion does

- Every object becomes an instance under `hull.objects.<type>` whose key is the object's name. `hull.config.general.noObjectNamePrefixes` is set so that names are rendered unchanged, and all references between objects (volumes, `env` and `envFrom` references, Ingress backends, HPA targets, ...) keep working as they are.
- Arrays that HULL models as dictionaries are converted to dictionaries: `containers`, `initContainers`, `volumes`, `env`, `envFrom`, `ports`, `volumeMounts`, Service `ports`, Ingress `rules`, `paths` and `tls`, and `webhooks`. The keys are the elements' names. Where the original order differs from the alphanumeric order of the keys, the elements get an `order` property so that they render in the original order.
- Container images are split into `registry`, `repository`, `tag` and `digest`.
- ConfigMap and Secret data become `data.<key>.inline` entries. Secret data is decoded to plain text where it is text; binary data stays base64 encoded with `preEncoded: true`. Content containing `{{` gets `noTemplating: true` so that HULL does not process it as a template.
- Workload selectors are kept with the explicit `selector` property, so the selectors of an existing release do not change. Pod template labels and annotations become `pod.labels` and `pod.annotations`.
- `null` fields and what the API server adds to live objects (`status`, `uid`, `resourceVersion`, `managedFields`, ...) are removed.
- The values start with a `# yaml-language-server: $schema=...` comment, so that editors validate them against the schema of the HULL version while editing.

Objects that HULL cannot render exactly as their native type become `generic` objects, which HULL renders exactly as given. The report says why for each of them. This happens for:

- kinds without a HULL object type, for example CustomResourceDefinitions and custom resources
- an `apiVersion` other than the one HULL renders for the kind, for example `policy/v1beta1` PodDisruptionBudgets
- Services without `selector`, which would get HULL's default selector
- Ingresses with backends other than a Service or TLS entries without `secretName`
- objects with fields HULL does not render for their kind, for example `jobTemplate.metadata` of a CronJob

## Reading the report

Notes are printed to stderr, and with `--report` written as JSON. `info` notes explain decisions that do not change the result, `warning` notes point to things that cannot be represented exactly and need attention, for example `metadata.finalizers`, labels with different values on an object and its pod template, or values that look like HULL transformations.

With `--verify`, every input object is reported as `identical`, `different` (with the differing fields), `missing` (not rendered) or `unexpected` (rendered but not in the input). Before comparing, these documented differences are normalized because HULL adds them by design and they do not change what Kubernetes does with the object:

| Normalization | Why |
| ------------- | --- |
| HULL standard labels added | HULL adds `app.kubernetes.io/name`, `instance`, `component`, `managed-by`, `version`, `part-of` and `helm.sh/chart` to objects and pod templates where they are not set. |
| Object labels and annotations added to the pod template | HULL renders an object's `labels` and `annotations` on its pod template too. |
| Namespace set | HULL sets `metadata.namespace` on namespaced objects and pod templates where the input had none. |
| Name and namespace set on a CronJob's job template | HULL renders `metadata` for the job template. |
| Pod template name not rendered | Kubernetes ignores `metadata.name` of pod templates. |
| Generated port names | HULL derives port names from dictionary keys, so unnamed ports get a name like `tcp-8080`. |
| Image tag dropped in favor of the digest | An image with a tag and a digest renders by digest only, Kubernetes pulls by digest in both cases. |
| `Opaque` Secret type, empty `value` of an environment variable, empty maps and lists | Kubernetes defaults. |

All other differences are reported. A verified conversion means: apart from the normalizations above, every object renders field by field as in the input.

## Making the result idiomatic

The converted values reproduce the input, but they do not yet use what makes HULL charts short and easy to maintain. With the verified conversion as a baseline, refactor in small steps and compare the rendering after each step with the baseline, for example with `helm template` and `diff`:

1. Replace values that repeat across objects, like image tags, registry names or resource sizes, by `_HT*` references to a single entry in `hull.config.specific`.
2. Move settings shared by several containers or objects to `_HULL_OBJECT_TYPE_DEFAULT_` or named `sources`, see [chart design](/hull/files/doc/chart_design.md).
3. When object names may change, which is the case for a new installation, remove `noObjectNamePrefixes` and shorten the keys, so that HULL derives `<release>-<chart>-<key>` names and references.
4. When the workloads may be recreated, remove the explicit `selector` properties and the pod labels that only served them, so that HULL generates matching selectors and labels. Services named like their workload then need no `selector` either.
5. Remove labels that duplicate HULL's standard labels.

Steps 3 and 4 change the rendered objects on purpose. Selectors of Deployments, StatefulSets and DaemonSets cannot be changed on an existing release, so only take these steps for new installations or after planning the migration.

---
Back to [README.md](/README.md)
