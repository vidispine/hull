# Development Notes

## Adding a new Kubernetes object type (Example: PriorityClass)

### Check which object template is right for the type to implement:
- `_objects_base_plain.tpl`: simple object without array structures that should be converted to dictionaries
- `_objects_base_rbac.tpl`: simple object without array structures that should be converted to dictionaries and subject to RBAC enablement
- `_objects_base_spec.tpl`: simple object without array structures that should be converted to dictionaries having a `spec` property
- `_objects_base_pod.tpl`: objects that internally use a pod template 
- `_objects_xyz.tpl`: any other more complex object with array structures that should be converted to dictionaries requires a custom template

[PriorityClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#priorityclass-v1-scheduling-k8s-io) is a very simple structure so it can use `_objects_base_plain.tpl`

### Add to the handled objects in `hull.yaml`

```yaml
{{- /*
### Load plain objects
*/ -}}
{{- $template := "hull.object.base.plain" }}
{{- $allObjects = merge $allObjects (dict "ServiceAccount" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "StorageClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "storage.k8s.io/v1")) }}
{{- $allObjects = merge $allObjects (dict "CustomResource" (dict "HULL_TEMPLATE" $template)) }}
{{- $allObjects = merge $allObjects (dict "PriorityClass" (dict "HULL_TEMPLATE" $template "API_VERSION" "scheduling.k8s.io/v1")) }}
```

### Add the defaults to `values.yaml`

```yaml
...

###################################################

# PODDISRUPTIONBUDGET
poddisruptionbudget :
    _HULL_OBJECT_TYPE_DEFAULT_:
    enabled: true
    annotations: {}
    labels: {}
###################################################

# PRIORITYCLASS
priorityclass :
    _HULL_OBJECT_TYPE_DEFAULT_:
    enabled: true
    annotations: {}
    labels: {}
###################################################
```

### Add the required information to the `values.schema.json`

- add root schema element (`priorityclass`)
- add referenced schema element from root schema element (`priorityclass.v1`)
- any K8S schema element that should be combined with HULL schema elements (eg. `#/definitions/hull.ObjectBase.v1`) needs to be prepared for this:
- remove the `additionalProperties: false` attribute so schema checking can handle coexistence of multiple schemas
- add a `.Names` schema element to list the allowed property names
- if referenced K8S schema element is a 'root' object remove the properties `apiVersion`, `kind` and `metadata` since the are handled by `#/definitions/hull.ObjectBase.v1`
    
```yaml
...

"priorityclass": {
    "$id": "#/definitions/root/objects/priorityclass",
    "title": "PriorityClass",
    "type": "object",
    "required": [],
    "patternProperties": {
    "^[^_].*$": {
        "type": [
        "null",
        "object"
        ],
        "anyOf": [
        {
            "type": "null"
        },
        {
            "$ref": "#/definitions/priorityclass.v1"
        }
        ],
        "properties": {}
    }
    }
}

...

"priorityclass.v1": {
    "$id": "#/definitions/priorityclass.v1",
    "title": "PriorityClass",
    "type": "object",
    "allOf": [
        {
        "$ref": "#/definitions/hull.ObjectBase.v1"
        },
        {
        "$ref": "#/definitions/io.k8s.api.scheduling.v1.PriorityClass"
        },
        {
        "propertyNames": {
            "anyOf": [
            {
                "$ref": "#/definitions/hull.ObjectBase.v1.Names"
            },
            {
                "$ref": "#/definitions/io.k8s.api.scheduling.v1.PriorityClass.Names"
            }
            ]
        }
        }        
    ]
    },

    ...

    "io.k8s.api.scheduling.v1.PriorityClass.Names":
    {
    "enum": [
        "description",
        "globalDefault",
        "preemptionPolicy",
        "value"
    ]
    },
    "io.k8s.api.scheduling.v1.PriorityClass": {
    "description": "PriorityClass defines mapping from a priority class name to the priority integer value. The value can be any valid integer.",
    "properties": {
        "description": {
        "description": "description is an arbitrary string that usually provides guidelines on when this priority class should be used.",
        "type": "string"
        },
        "globalDefault": {
        "description": "globalDefault specifies whether this PriorityClass should be considered as the default priority for pods that do not have any priority class. Only one PriorityClass can be marked as `globalDefault`. However, if more than one PriorityClasses exists with their `globalDefault` field set to true, the smallest value of such global default PriorityClasses will be used as the default priority.",
        "type": "boolean"
        },
        "preemptionPolicy": {
        "description": "PreemptionPolicy is the Policy for preempting pods with lower priority. One of Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if unset. This field is beta-level, gated by the NonPreemptingPriority feature-gate.",
        "type": "string"
        },
        "value": {
        "description": "The value of this priority class. This is the actual priority that pods receive when they have the name of this class in their pod spec.",
        "format": "int32",
        "type": "integer"
        }
    },
    "required": [
        "value"
    ],
    "type": "object",
    "x-kubernetes-group-version-kind": [
        {
        "group": "scheduling.k8s.io",
        "kind": "PriorityClass",
        "version": "v1"
        }
    ]
    },

    ...
```
### Add tests for object type

- Create folder at `files/test/HULL/sources/cases` for object type (eg. `files/test/HULL/sources/priorityclass`)
- add `hull.values.yaml` with test cases
- write the test spec at `files/test/HULL/specs` (eg. `files/test/HULL/specs/priorityclass,spec`) and define tests

### Add documentation to the `README.md`

- add to the available object types and if needed add further documentation.