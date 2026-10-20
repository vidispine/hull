#!/usr/bin/env python3
"""Convert Kubernetes manifests into HULL values and verify the conversion.

Reads Kubernetes objects from YAML files, directories or stdin, for example the
output of `helm template` of an existing chart, and writes HULL values that render
the same objects. With --chart a complete HULL based chart is written. With --verify
the result is rendered with helm and compared object by object with the input, so a
conversion can be trusted without reading it line by line.

The conversion is deterministic and keeps everything that matters to Kubernetes:
names, namespaces, labels, selectors, field values and the order of array elements.
Arrays that HULL models as dictionaries (containers, env, ports, volumes, ...) are
converted to dictionaries, using 'order' where the original order differs from the
alphanumeric key order. Objects HULL cannot represent exactly as a native object type,
for example custom resources or a Service without selector, become 'generic' objects
that render exactly as given. Each such decision is reported.

Requirements: Python 3.8+ and PyYAML. --verify also requires helm.

Examples:
  helm template my-release ./old-chart | hull_import.py --chart ./new-chart --verify -
  hull_import.py -o values.yaml manifests/
"""

import argparse
import base64
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

HULL_REPOSITORY = "https://vidispine.github.io/hull"

# kind -> (HULL object type, apiVersion HULL renders, layout)
# layout 'plain': the object's fields are given at the top level of the HULL object
# layout 'spec':  the fields of the object's 'spec' are given at the top level
# other layouts have a dedicated conversion
NATIVE_TYPES = {
    "Namespace": ("namespace", "v1", "plain"),
    "ServiceAccount": ("serviceaccount", "v1", "plain"),
    "StorageClass": ("storageclass", "storage.k8s.io/v1", "plain"),
    "PriorityClass": ("priorityclass", "scheduling.k8s.io/v1", "plain"),
    "Endpoints": ("endpoints", "v1", "plain"),
    "EndpointSlice": ("endpointslice", "discovery.k8s.io/v1", "plain"),
    "MutatingWebhookConfiguration": ("mutatingwebhookconfiguration", "admissionregistration.k8s.io/v1", "webhooks"),
    "ValidatingWebhookConfiguration": ("validatingwebhookconfiguration", "admissionregistration.k8s.io/v1", "webhooks"),
    "Role": ("role", "rbac.authorization.k8s.io/v1", "plain"),
    "ClusterRole": ("clusterrole", "rbac.authorization.k8s.io/v1", "plain"),
    "RoleBinding": ("rolebinding", "rbac.authorization.k8s.io/v1", "plain"),
    "ClusterRoleBinding": ("clusterrolebinding", "rbac.authorization.k8s.io/v1", "plain"),
    "PersistentVolume": ("persistentvolume", "v1", "spec"),
    "PersistentVolumeClaim": ("persistentvolumeclaim", "v1", "spec"),
    "ServiceMonitor": ("servicemonitor", "monitoring.coreos.com/v1", "spec"),
    "PodDisruptionBudget": ("poddisruptionbudget", "policy/v1", "spec"),
    "ResourceQuota": ("resourcequota", "v1", "spec"),
    "NetworkPolicy": ("networkpolicy", "networking.k8s.io/v1", "spec"),
    "IngressClass": ("ingressclass", "networking.k8s.io/v1", "spec"),
    "LimitRange": ("limitrange", "v1", "spec"),
    "HorizontalPodAutoscaler": ("horizontalpodautoscaler", "autoscaling/v2", "spec"),
    "MutatingAdmissionPolicy": ("mutatingadmissionpolicy", "admissionregistration.k8s.io/v1", "spec"),
    "MutatingAdmissionPolicyBinding": ("mutatingadmissionpolicybinding", "admissionregistration.k8s.io/v1", "spec"),
    "ValidatingAdmissionPolicy": ("validatingadmissionpolicy", "admissionregistration.k8s.io/v1", "spec"),
    "ValidatingAdmissionPolicyBinding": ("validatingadmissionpolicybinding", "admissionregistration.k8s.io/v1", "spec"),
    "Deployment": ("deployment", "apps/v1", "workload"),
    "DaemonSet": ("daemonset", "apps/v1", "workload"),
    "StatefulSet": ("statefulset", "apps/v1", "workload"),
    "Job": ("job", "batch/v1", "job"),
    "CronJob": ("cronjob", "batch/v1", "cronjob"),
    "ConfigMap": ("configmap", "v1", "configmap"),
    "Secret": ("secret", "v1", "secret"),
    "Service": ("service", "v1", "service"),
    "Ingress": ("ingress", "networking.k8s.io/v1", "ingress"),
}

# Labels HULL adds to every object (and pod template) unless the object defines them
HULL_STANDARD_LABELS = {
    "app.kubernetes.io/name", "app.kubernetes.io/instance", "app.kubernetes.io/component",
    "app.kubernetes.io/managed-by", "app.kubernetes.io/version", "app.kubernetes.io/part-of",
    "helm.sh/chart", "vidispine.hull/version",
}

SERVER_METADATA = ("uid", "resourceVersion", "generation", "creationTimestamp", "managedFields",
                   "selfLink", "deletionTimestamp", "deletionGracePeriodSeconds")
UNSUPPORTED_METADATA = ("finalizers", "ownerReferences", "generateName")

HULL_TRANSFORMATION = re.compile(r"^\s*(_HT[*?^!&/]|_HULL_TRANSFORMATION_<<<)")


class Note:
    """A remark about the conversion of one object, shown in the report."""

    def __init__(self, level, ref, message):
        self.level = level          # 'info' or 'warning'
        self.ref = ref              # 'Kind/name'
        self.message = message

    def as_dict(self):
        return {"level": self.level, "object": self.ref, "message": self.message}


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------

def load_objects(inputs):
    """Load all Kubernetes objects from files, directories or '-' (stdin)."""
    objects = []
    for source in inputs:
        if source == "-":
            objects += parse_documents(sys.stdin.read(), "<stdin>")
        elif os.path.isdir(source):
            for root, _, files in sorted(os.walk(source)):
                for name in sorted(files):
                    if name.endswith((".yaml", ".yml", ".json")):
                        path = os.path.join(root, name)
                        with open(path, encoding="utf-8") as file:
                            objects += parse_documents(file.read(), path)
        else:
            with open(source, encoding="utf-8") as file:
                objects += parse_documents(file.read(), source)
    return objects


def parse_documents(text, origin):
    result = []
    for document in yaml.safe_load_all(text):
        if not document:
            continue
        if not isinstance(document, dict) or "kind" not in document:
            raise ValueError(f"{origin}: not a Kubernetes object: {str(document)[:80]}")
        if document["kind"].endswith("List") and isinstance(document.get("items"), list):
            result += [item for item in document["items"] if item]
        else:
            result.append(document)
    return result


def drop_nulls(value):
    if isinstance(value, dict):
        return {k: drop_nulls(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [drop_nulls(v) for v in value if v is not None]
    return value


def clean(obj):
    """Remove what the API server adds, so dumps of live objects can be imported too.
    Null fields are removed as well, Kubernetes treats them like absent fields."""
    obj = drop_nulls(copy.deepcopy(obj))
    obj.pop("status", None)
    metadata = obj.setdefault("metadata", {})
    for key in SERVER_METADATA:
        metadata.pop(key, None)
    annotations = metadata.get("annotations") or {}
    annotations.pop("kubectl.kubernetes.io/last-applied-configuration", None)
    if not annotations:
        metadata.pop("annotations", None)
    return obj


# --------------------------------------------------------------------------------------
# Conversion
# --------------------------------------------------------------------------------------

class Converter:

    def __init__(self, namespace=None):
        self.namespace = namespace
        self.notes = []
        self.objects = {}           # HULL object type -> key -> spec
        self.origin = {}            # (HULL object type, key) -> original object
        self.generated_port_names = {}

    def note(self, level, obj, message):
        self.notes.append(Note(level, ref(obj), message))

    # ---- entry point ------------------------------------------------------------------

    def convert(self, objects):
        for obj in objects:
            obj = clean(obj)
            kind = obj.get("kind")
            hull_type, api_version, layout = NATIVE_TYPES.get(kind, ("generic", None, "generic"))
            if layout == "generic":
                self.note("info", obj, f"HULL has no object type for a {kind}, imported as generic object")
            elif obj.get("apiVersion") != api_version:
                self.note("info", obj, f"apiVersion {obj.get('apiVersion')} differs from {api_version} "
                                       f"that HULL renders for a {kind}, imported as generic object")
                hull_type, layout = "generic", "generic"
            notes, ports = len(self.notes), copy.deepcopy(self.generated_port_names)
            try:
                spec = self.convert_object(obj, layout)
            except Fallback as fallback:
                del self.notes[notes:]
                self.generated_port_names = ports
                self.note("info", obj, f"{fallback}, imported as generic object")
                hull_type, spec = "generic", self.convert_object(obj, "generic")
            self.add(hull_type, obj, spec)
        general = {"noObjectNamePrefixes": True}
        if "default" in self.objects.get("serviceaccount", {}):
            # an imported 'default' ServiceAccount enables HULL's 'default' instance, which would
            # otherwise be assigned to all pods without serviceAccountName
            general["assignDefaultServiceAccountToPods"] = False
        values = {"hull": {"config": {"general": general}, "objects": self.objects}}
        self.check_transformation_lookalikes(values)
        return values

    def add(self, hull_type, obj, spec):
        name = obj["metadata"].get("name", "")
        instances = self.objects.setdefault(hull_type, {})
        key = name
        if key in instances or (hull_type in ("serviceaccount", "role", "rolebinding") and key == "default"):
            if key in instances:
                key = unique_key(f"{name}-{obj['kind'].lower()}", instances)
                spec = {"metadataNameOverride": name, **spec}
            if key == "default":
                # HULL predefines a 'default' instance that is coupled to createDefaultRbacTriplet
                spec = {"enabled": True, **spec}
        if name != name.lower():
            self.note("warning", obj, "HULL renders object names in lowercase, the name will change")
        instances[key] = spec
        self.origin[(hull_type, key)] = obj

    def convert_object(self, obj, layout):
        metadata = obj.get("metadata") or {}
        spec = {}
        if layout == "generic":
            spec["apiVersion"] = obj.get("apiVersion")
            spec["kind"] = obj.get("kind")
        if metadata.get("labels"):
            spec["labels"] = dict(metadata["labels"])
        if metadata.get("annotations"):
            spec["annotations"] = dict(metadata["annotations"])
        namespace = metadata.get("namespace")
        if namespace and namespace != self.namespace:
            spec["namespaceOverride"] = namespace
        for key in UNSUPPORTED_METADATA:
            if metadata.get(key):
                self.note("warning", obj, f"metadata.{key} cannot be rendered by HULL and is dropped")
        body = {k: v for k, v in obj.items() if k not in ("apiVersion", "kind", "metadata")}
        if layout in ("plain", "generic"):
            spec.update(body)
        elif layout == "spec":
            spec.update(self.spec_fields(obj, body))
        else:
            getattr(self, f"convert_{layout}")(obj, body, spec)
        return spec

    def spec_fields(self, obj, body):
        others = [k for k in body if k != "spec"]
        if others:
            raise Fallback(f"fields {', '.join(others)} outside of 'spec' are not rendered by HULL")
        return dict(body.get("spec") or {})

    # ---- workloads ----------------------------------------------------------------------

    def convert_workload(self, obj, body, spec):
        fields = self.spec_fields(obj, body)
        template = fields.pop("template", None) or {}
        selector = fields.pop("selector", None)
        if selector is not None:
            spec["selector"] = selector
        spec.update(fields)
        spec["pod"] = self.convert_template(obj, template, spec)

    def convert_job(self, obj, body, spec):
        fields = self.spec_fields(obj, body)
        template = fields.pop("template", None) or {}
        spec.update(fields)
        spec["pod"] = self.convert_template(obj, template, spec)

    def convert_cronjob(self, obj, body, spec):
        fields = self.spec_fields(obj, body)
        job_template = fields.pop("jobTemplate", None) or {}
        if job_template.get("metadata"):
            raise Fallback("jobTemplate.metadata is not rendered by HULL")
        job_fields = dict(job_template.get("spec") or {})
        template = job_fields.pop("template", None) or {}
        spec.update(fields)
        # the job template and its pod template take their metadata from 'job', not from the CronJob
        job = dict(job_fields)
        job["pod"] = self.convert_template(obj, template, job)
        spec["job"] = {"labels": job.pop("labels"), **job} if "labels" in job else job

    def convert_template(self, obj, template, spec):
        """Convert a pod template. 'spec' is the HULL dictionary whose 'labels' HULL also renders
        on the pod template, the object itself or the 'job' of a CronJob."""
        template_metadata = template.get("metadata") or {}
        pod = self.convert_pod_spec(obj, template.get("spec") or {})
        labels = template_metadata.get("labels") or {}
        object_labels = dict(spec.get("labels") or {})
        pod_labels, moved = {}, []
        for key, value in labels.items():
            if key in object_labels:
                if object_labels[key] != value:
                    self.note("warning", obj, f"label {key} has different values on the object and the pod "
                                              f"template, HULL renders the object's value on both")
                continue
            if key in HULL_STANDARD_LABELS:
                # On the pod template HULL's standard labels take precedence over pod.labels,
                # only object labels take precedence over them
                object_labels[key] = value
                moved.append(key)
                continue
            pod_labels[key] = value
        if moved:
            spec["labels"] = object_labels
            self.note("info", obj, f"pod template labels {', '.join(moved)} are set as object labels to take "
                                   f"precedence over HULL's standard labels, they are rendered on the object too")
        extra = [k for k in object_labels if k not in labels and k not in moved]
        if extra:
            self.note("info", obj, f"HULL also renders the object labels {', '.join(sorted(extra))} on the pod template")
        if template_metadata.get("annotations"):
            pod = {"annotations": dict(template_metadata["annotations"]), **pod}
        if pod_labels:
            pod = {"labels": pod_labels, **pod}
        if template_metadata.get("name"):
            self.note("info", obj, "the pod template's metadata.name is not rendered, Kubernetes ignores it")
        for key in template_metadata:
            if key not in ("labels", "annotations", "name", "namespace", "creationTimestamp"):
                self.note("warning", obj, f"template.metadata.{key} cannot be rendered by HULL and is dropped")
        return pod

    def convert_pod_spec(self, obj, pod_spec):
        pod = {}
        used_port_names = {port.get("name") for kind in ("containers", "initContainers")
                           for container in pod_spec.get(kind) or [] for port in container.get("ports") or []}
        for field, value in pod_spec.items():
            if field in ("containers", "initContainers"):
                pod[field] = to_hull_dict(value or [], lambda c: c["name"],
                                          lambda c: self.convert_container(obj, c, used_port_names))
            elif field == "volumes":
                pod[field] = to_hull_dict(value or [], lambda v: v["name"], without("name"))
            elif field in ("labels", "annotations"):
                raise Fallback(f"the pod spec field {field} collides with HULL's pod metadata")
            else:
                pod[field] = value
        return pod

    def convert_container(self, obj, container, used_port_names):
        result = {}
        for field, value in container.items():
            if field == "name":
                continue
            if field == "image":
                result["image"] = parse_image(value)
                if result["image"].get("digest") and result["image"].get("tag"):
                    self.note("info", obj, f"image {value} has a tag and a digest, HULL renders it by digest only")
            elif field == "env":
                names = [e["name"] for e in value or []]
                # a later definition of the same variable wins in Kubernetes, the key can exist only once
                last = [e for i, e in enumerate(value or []) if e["name"] not in names[i + 1:]]
                if len(last) != len(names):
                    self.note("warning", obj, f"container {container['name']} defines an env variable more than "
                                              f"once, only the last definition is kept")
                result["env"] = to_hull_dict(last, lambda e: e["name"], self.convert_env)
            elif field == "envFrom":
                result["envFrom"] = to_hull_dict(value or [], env_from_key, lambda e: dict(e))
            elif field == "ports":
                result["ports"] = to_hull_dict(value or [], lambda p: self.port_name(obj, container, p, used_port_names),
                                               without("name"))
            elif field == "volumeMounts":
                result["volumeMounts"] = to_hull_dict(value or [], lambda m: m["name"], lambda m: dict(m))
            elif field in ("enabled", "order", "sources"):
                raise Fallback(f"the container field {field} collides with a HULL property")
            else:
                result[field] = value
        if "image" not in result:
            self.note("warning", obj, f"container {container['name']} has no image, rendering it fails unless "
                                      f"hull.config.general.errorChecks.containerImageValid is false")
        return result

    @staticmethod
    def convert_env(env):
        result = {k: v for k, v in env.items() if k != "name"}
        if "value" not in result and "valueFrom" not in result:
            result["value"] = ""
        return result

    def port_name(self, obj, container, port, used_port_names):
        if port.get("name"):
            return port["name"]
        base = f"{str(port.get('protocol', 'TCP')).lower()}-{port.get('containerPort')}"
        name, index = base, 2
        while name in used_port_names:
            name, index = f"{base}-{index}", index + 1
        used_port_names.add(name)
        self.generated_port_names.setdefault(ref(obj), set()).add(name)
        self.note("info", obj, f"unnamed port {port.get('containerPort')} of container {container['name']} "
                               f"gets the name {name}, HULL derives port names from keys")
        return name

    # ---- webhook configurations ----------------------------------------------------------

    def convert_webhooks(self, obj, body, spec):
        webhooks = body.pop("webhooks", None)
        spec.update(body)
        if webhooks:
            # HULL takes the webhook's name from its 'name' property, not from the key
            spec["webhooks"] = to_hull_dict(webhooks, lambda w: w["name"], lambda w: dict(w))

    # ---- service, ingress ---------------------------------------------------------------

    def convert_service(self, obj, body, spec):
        fields = self.spec_fields(obj, body)
        if not fields.get("selector"):
            raise Fallback("a Service without selector gets a default selector in HULL")
        ports = fields.pop("ports", None)
        spec.update(fields)
        if ports:
            used = {p.get("name") for p in ports}
            spec["ports"] = to_hull_dict(ports, lambda p: self.service_port_name(obj, p, used), without("name"))

    def service_port_name(self, obj, port, used):
        if port.get("name"):
            return port["name"]
        base = f"{str(port.get('protocol', 'TCP')).lower()}-{port.get('port')}"
        name, index = base, 2
        while name in used:
            name, index = f"{base}-{index}", index + 1
        used.add(name)
        self.generated_port_names.setdefault(ref(obj), set()).add(name)
        self.note("info", obj, f"unnamed service port {port.get('port')} gets the name {name}, "
                               f"HULL derives port names from keys")
        return name

    def convert_ingress(self, obj, body, spec):
        fields = self.spec_fields(obj, body)
        rules = fields.pop("rules", None)
        tls = fields.pop("tls", None)
        spec.update(fields)
        for entry in tls or []:
            if not entry.get("secretName"):
                raise Fallback("a TLS entry without secretName is not rendered correctly by HULL")
        for rule in rules or []:
            if set(rule) - {"host", "http"} or not rule.get("http"):
                raise Fallback("an Ingress rule without http paths is not rendered by HULL")
            for path in rule["http"].get("paths") or []:
                if "service" not in (path.get("backend") or {}):
                    raise Fallback("an Ingress backend other than a service is not rendered by HULL")
        if tls:
            spec["tls"] = to_hull_dict(tls, lambda t: t["secretName"], lambda t: dict(t))
        if rules:
            spec["rules"] = to_hull_dict(rules, lambda r: r.get("host") or "default", self.convert_ingress_rule)

    @staticmethod
    def convert_ingress_rule(rule):
        result = {}
        if rule.get("host"):
            result["host"] = rule["host"]
        result["http"] = {"paths": to_hull_dict(rule["http"].get("paths") or [],
                                                lambda p: p.get("path") or "default", lambda p: dict(p))}
        return result

    # ---- configmap, secret --------------------------------------------------------------

    def convert_configmap(self, obj, body, spec):
        data = body.pop("data", None)
        spec.update(body)
        if data:
            spec["data"] = {key: self.inline(obj, key, value) for key, value in data.items()}

    def convert_secret(self, obj, body, spec):
        data = body.pop("data", None)
        spec.update(body)
        if data:
            spec["data"] = {}
            for key, encoded in data.items():
                text = decode_text(encoded)
                if text is None:
                    spec["data"][key] = {"inline": encoded, "preEncoded": True}
                else:
                    spec["data"][key] = self.inline(obj, key, text)

    def inline(self, obj, key, value):
        entry = {"inline": "" if value is None else str(value)}
        if "{{" in entry["inline"]:
            entry["noTemplating"] = True
        return entry

    # ---- checks ---------------------------------------------------------------------------

    def check_transformation_lookalikes(self, values):
        for hull_type, instances in self.objects.items():
            for key, spec in instances.items():
                for path, value in walk_strings(spec):
                    if HULL_TRANSFORMATION.match(value):
                        self.notes.append(Note("warning", ref(self.origin[(hull_type, key)]),
                                               f"value at {path} looks like a HULL transformation and "
                                               f"will be processed as one"))


class Fallback(Exception):
    """Raised when an object cannot be represented exactly by its native HULL type."""


def ref(obj):
    return f"{obj.get('kind')}/{(obj.get('metadata') or {}).get('name')}"


def without(field):
    return lambda item: {k: v for k, v in item.items() if k != field}


def env_from_key(entry):
    for ref_type in ("configMapRef", "secretRef"):
        if entry.get(ref_type, {}).get("name"):
            return f"{entry[ref_type]['name']}{'-' + entry['prefix'] if entry.get('prefix') else ''}"
    return "envfrom"


def unique_key(key, existing):
    candidate, index = key, 2
    while candidate in existing:
        candidate, index = f"{key}-{index}", index + 1
    return candidate


def to_hull_dict(items, key_of, convert):
    """Turn a Kubernetes array into a HULL dictionary that renders in the same order."""
    result, keys = {}, []
    for item in items:
        key = unique_key(str(key_of(item)), result)
        result[key] = convert(item)
        keys.append(key)
    if keys != sorted(keys):
        for index, key in enumerate(keys):
            result[key] = {**result[key], "order": index}
    return result


IMAGE_REFERENCE = re.compile(r"^(?:(?P<registry>[^/]+)/)?(?P<repository>[^:@]+(?:/[^:@]+)*)"
                             r"(?::(?P<tag>[^@]+))?(?:@(?P<digest>.+))?$")


def parse_image(image):
    """Split an image reference into the HULL image properties."""
    match = IMAGE_REFERENCE.match(str(image))
    if not match:
        return {"repository": str(image)}
    registry = match.group("registry")
    repository = match.group("repository")
    # The first component is a registry only if it looks like a host, like Docker does
    if registry and not ("." in registry or ":" in registry or registry == "localhost"):
        repository, registry = f"{registry}/{repository}", None
    result = {}
    if registry:
        result["registry"] = registry
    result["repository"] = repository
    if match.group("tag"):
        result["tag"] = match.group("tag")
    if match.group("digest"):
        result["digest"] = match.group("digest")
    return result


def decode_text(encoded):
    """Return the decoded text of base64 Secret data, or None if it is binary."""
    try:
        raw = base64.b64decode(str(encoded), validate=True)
        text = raw.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    if base64.b64encode(raw).decode("ascii") != str(encoded):
        return None
    if any(ord(c) < 32 and c not in "\n\r\t" for c in text):
        return None
    return text


def walk_strings(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

class Dumper(yaml.SafeDumper):

    def ignore_aliases(self, data):
        return True


def represent_str(dumper, value):
    if "\n" in value and not any(c in value for c in "\t") and value == value.rstrip(" "):
        return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", value)


Dumper.add_representer(str, represent_str)


def dump(data):
    return yaml.dump(data, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=4096,
                     default_flow_style=False)


def hull_chart_version(hull_path):
    with open(os.path.join(hull_path, "Chart.yaml"), encoding="utf-8") as file:
        return str(yaml.safe_load(file)["version"])


def write_chart(directory, chart_name, values, hull_path):
    """Write a HULL based chart. The HULL library is copied to charts/hull for offline use."""
    os.makedirs(os.path.join(directory, "templates"), exist_ok=True)
    version = hull_chart_version(hull_path)
    chart = {"apiVersion": "v2", "name": chart_name, "version": "0.1.0", "type": "application",
             "dependencies": [{"name": "hull", "version": version, "repository": HULL_REPOSITORY}]}
    with open(os.path.join(directory, "Chart.yaml"), "w", encoding="utf-8") as file:
        file.write(dump(chart))
    with open(os.path.join(directory, "values.yaml"), "w", encoding="utf-8") as file:
        file.write(dump(values))
    with open(os.path.join(directory, "templates", "hull.yaml"), "w", encoding="utf-8") as file:
        file.write('{{- include "hull.objects.prepare.all" (dict "HULL_ROOT_KEY" "hull" "ROOT_CONTEXT" $) }}\n')
    target = os.path.join(directory, "charts", "hull")
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    for name in ("Chart.yaml", "values.yaml", "values.schema.json"):
        shutil.copy(os.path.join(hull_path, name), target)
    shutil.copytree(os.path.join(hull_path, "templates"), os.path.join(target, "templates"))


# --------------------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------------------

def render(helm, chart_dir, release, namespace, kube_version):
    command = [helm, "template", release, chart_dir, "--namespace", namespace]
    if kube_version:
        command += ["--kube-version", kube_version]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"rendering the converted chart failed:\n{result.stderr or result.stdout}")
    return [obj for obj in yaml.safe_load_all(result.stdout) if obj]


def prune(value):
    """Drop nulls and empty labels and annotations, which Kubernetes treats like absent fields.
    Other empty maps and lists are kept, some of them carry meaning, like 'emptyDir: {}'."""
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            item = prune(item)
            if item is None or (key in ("labels", "annotations") and item == {}):
                continue
            result[key] = item
        return result
    if isinstance(value, list):
        return [prune(item) for item in value if item is not None]
    return value


def normalize_pair(original, rendered, generated_port_names):
    """Apply the documented normalizations, returning both objects and what was normalized."""
    original, rendered = prune(clean(original)), prune(copy.deepcopy(rendered))
    normalized = set()
    original_metadata = original.setdefault("metadata", {})
    rendered_metadata = rendered.setdefault("metadata", {})
    if "namespace" not in original_metadata and rendered_metadata.pop("namespace", None) is not None:
        normalized.add("namespace set to the release namespace")
    object_annotations = original_metadata.get("annotations") or {}
    for path in [("spec", "template", "metadata"), ("spec", "jobTemplate", "spec", "template", "metadata")]:
        template_metadata = dig(rendered, path)
        original_template = dig(original, path) or {}
        if not isinstance(template_metadata, dict):
            continue
        if "namespace" not in original_template and template_metadata.pop("namespace", None) is not None:
            normalized.add("namespace set on the pod template")
        if original_template.pop("name", None) is not None:
            normalized.add("pod template name not rendered")
        annotations = template_metadata.get("annotations") or {}
        for key in list(annotations):
            if key not in (original_template.get("annotations") or {}) and object_annotations.get(key) == annotations[key]:
                del annotations[key]
                normalized.add("object annotations added to the pod template")
        if "annotations" in template_metadata and not annotations:
            del template_metadata["annotations"]
    object_labels = original_metadata.get("labels") or {}
    job_template_metadata = dig(rendered, ("spec", "jobTemplate", "metadata"))
    if isinstance(job_template_metadata, dict):
        original_job_template = dig(original, ("spec", "jobTemplate", "metadata")) or {}
        for key in ("name", "namespace"):
            if key not in original_job_template and job_template_metadata.pop(key, None) is not None:
                normalized.add("name and namespace set on the job template")
    label_paths = [("metadata",), ("spec", "template", "metadata"), ("spec", "jobTemplate", "metadata"),
                   ("spec", "jobTemplate", "spec", "template", "metadata")]
    for path in label_paths:
        original_labels = dig(original, path + ("labels",)) or {}
        rendered_labels = dig(rendered, path + ("labels",))
        if isinstance(rendered_labels, dict):
            for key in list(rendered_labels):
                if key in original_labels:
                    continue
                if key in HULL_STANDARD_LABELS:
                    del rendered_labels[key]
                    normalized.add("HULL standard labels added")
                elif path != ("metadata",) and object_labels.get(key) == rendered_labels[key]:
                    del rendered_labels[key]
                    normalized.add("object labels added to the pod template")
            if not rendered_labels:
                dig(rendered, path).pop("labels")
    if original.get("kind") == "Secret" and rendered.get("type") == "Opaque" and "type" not in original:
        rendered.pop("type")
    if original.get("kind") in ("Secret", "ConfigMap") and "data" not in original and rendered.get("data") == {}:
        rendered.pop("data")
    for path in [("spec", "template", "spec"), ("spec", "jobTemplate", "spec", "template", "spec")]:
        for container_type in ("containers", "initContainers"):
            originals = dig(original, path + (container_type,)) or []
            renders = dig(rendered, path + (container_type,)) or []
            for original_container, rendered_container in zip(originals, renders):
                normalize_container(original_container, rendered_container, generated_port_names, normalized)
    for original_port, rendered_port in zip(dig(original, ("spec", "ports")) or [], dig(rendered, ("spec", "ports")) or []):
        if "name" not in original_port and rendered_port.get("name") in generated_port_names:
            rendered_port.pop("name")
            normalized.add("generated port names")
    for path in [("spec", "template", "metadata"), ("spec", "jobTemplate", "metadata"),
                 ("spec", "jobTemplate", "spec", "template", "metadata")]:
        rendered_parent, original_parent = dig(rendered, path[:-1]), dig(original, path[:-1])
        if isinstance(rendered_parent, dict) and rendered_parent.get(path[-1]) == {} and not dig(original, path):
            del rendered_parent[path[-1]]
            if isinstance(original_parent, dict):
                original_parent.pop(path[-1], None)
    return prune(original), prune(rendered), sorted(normalized)


def normalize_container(original, rendered, generated_port_names, normalized):
    for original_env in original.get("env") or []:
        if "value" not in original_env and "valueFrom" not in original_env:
            original_env["value"] = ""
    for original_port, rendered_port in zip(original.get("ports") or [], rendered.get("ports") or []):
        if "name" not in original_port and rendered_port.get("name") in generated_port_names:
            rendered_port.pop("name")
            normalized.add("generated port names")
    image = parse_image(original.get("image", ""))
    if image.get("tag") and image.get("digest") and "@" in str(rendered.get("image", "")):
        original["image"] = str(original["image"]).replace(f":{image['tag']}@", "@")
        normalized.add("image tag dropped in favor of the digest")


def dig(value, path):
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def diff(original, rendered, path=""):
    """Yield (path, original, rendered) for every difference."""
    if isinstance(original, dict) and isinstance(rendered, dict):
        for key in list(original) + [k for k in rendered if k not in original]:
            yield from diff(original.get(key), rendered.get(key), f"{path}.{key}" if path else key)
    elif isinstance(original, list) and isinstance(rendered, list) and len(original) == len(rendered):
        for index, (a, b) in enumerate(zip(original, rendered)):
            yield from diff(a, b, f"{path}[{index}]")
    elif original != rendered:
        yield path, original, rendered


def verify(originals, rendered_objects, generated_port_names):
    by_identity = {}
    for obj in rendered_objects:
        by_identity.setdefault((obj.get("kind"), obj["metadata"].get("name")), []).append(obj)
    results = []
    for original in originals:
        original = clean(original)
        identity = (original.get("kind"), original["metadata"].get("name"))
        candidates = by_identity.get(identity) or []
        namespace = original["metadata"].get("namespace")
        matching = [c for c in candidates if not namespace or c["metadata"].get("namespace") in (namespace, None)]
        if not matching:
            results.append({"object": ref(original), "status": "missing", "differences": []})
            continue
        rendered = matching[0]
        candidates.remove(rendered)
        a, b, normalized = normalize_pair(original, rendered, generated_port_names.get(ref(original), set()))
        differences = [{"path": p, "original": x, "rendered": y} for p, x, y in diff(a, b)]
        results.append({"object": ref(original), "status": "different" if differences else "identical",
                        "normalized": normalized, "differences": differences})
    for leftovers in by_identity.values():
        for obj in leftovers:
            results.append({"object": ref(obj), "status": "unexpected", "differences": []})
    return results


def print_report(notes, results, stream):
    for note in notes:
        print(f"[{note.level}] {note.ref}: {note.message}", file=stream)
    if results is None:
        return
    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        if result["status"] != "identical":
            print(f"[{result['status']}] {result['object']}", file=stream)
            for d in result["differences"]:
                print(f"    {d['path']}: {json.dumps(d['original'])} -> {json.dumps(d['rendered'])}", file=stream)
    summary = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))
    print(f"Verification: {summary}", file=stream)


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------

def default_hull_path():
    candidate = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    return candidate if os.path.isfile(os.path.join(candidate, "templates", "_objects.tpl")) else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="\n\n".join(__doc__.split("\n\n")[1:]))
    parser.add_argument("inputs", nargs="+", help="YAML files, directories or - for stdin")
    parser.add_argument("-o", "--output", help="write the values to this file instead of stdout")
    parser.add_argument("--chart", help="write a complete HULL based chart to this directory")
    parser.add_argument("--chart-name", help="name of the written chart (default: directory name)")
    parser.add_argument("--hull", default=default_hull_path(),
                        help="path to the HULL chart directory (default: the HULL chart containing this script)")
    parser.add_argument("--verify", action="store_true",
                        help="render the converted chart with helm and compare it with the input")
    parser.add_argument("--release-name", default="release-name", help="release name used for --verify")
    parser.add_argument("--namespace", default="default",
                        help="namespace the input was rendered for; objects in it need no namespaceOverride")
    parser.add_argument("--kube-version", help="Kubernetes version passed to helm template for --verify")
    parser.add_argument("--helm", default="helm", help="helm binary used for --verify")
    parser.add_argument("--report", help="write the notes and the verification result as JSON to this file")
    args = parser.parse_args(argv)

    objects = load_objects(args.inputs)
    converter = Converter(namespace=args.namespace)
    values = converter.convert(objects)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(dump(values))
    elif not args.chart:
        sys.stdout.write(dump(values))

    results = None
    if args.chart or args.verify:
        if not args.hull:
            parser.error("--hull is required to write a chart or to verify")
        chart_dir = args.chart or tempfile.mkdtemp(prefix="hull-import-")
        chart_name = args.chart_name or os.path.basename(os.path.abspath(chart_dir)).lower()
        if not re.match(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", chart_name):
            chart_name = "imported"
        write_chart(chart_dir, chart_name, values, args.hull)
        try:
            if args.verify:
                rendered = render(args.helm, chart_dir, args.release_name, args.namespace, args.kube_version)
                results = verify(objects, rendered, converter.generated_port_names)
        finally:
            if not args.chart:
                shutil.rmtree(chart_dir, ignore_errors=True)

    print_report(converter.notes, results, sys.stderr)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as file:
            json.dump({"notes": [n.as_dict() for n in converter.notes], "verification": results}, file, indent=2)
    if results is not None and any(r["status"] != "identical" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)
