# Development Notes

## Adding a new Kubernetes object type (Example: PriorityClass)

### Check which object template is right for the type to implement:
- `_objects_base_plain.tpl`: simple object without array structures that should be converted to dictionaries
- `_objects_base_rbac.tpl`: simple object without array structures that should be converted to dictionaries and subject to RBAC enablement
- `_objects_base_spec.tpl`: simple object without array structures that should be converted to dictionaries having a `spec` property
- `_objects_base_pod.tpl`: objects that internally use a pod template 
- `_objects_xyz.tpl`: any other more complex object with array structures that should be converted to dictionaries requires a custom template

[PriorityClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#priorityclass-v1-scheduling-k8s-io) is a very simple structure so it can use `_objects_base_plain.tpl`

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

## Creating a release branch for a new Kubernetes version

### Create branch

Branch must be named `release-1.x` where x is the minor version of the Kubernetes release. Switch to this branch.

### Create JSON schema 

Create new matching JSON schema files in the `kubernetes-json-schema` folder with the instructions given in the [README.md](./../../kubernetes-json-schema/README.md) there. Patch version can be the highest available. It is expected no object properties are changed between patch versions.

### Adapt the JSON schema

Copy the `_definition.json` from the newly created schema folder to `values.schema.json` in the `hull` charts root library overwriting the existing content. Compare the `values.schema.json` content with that of the previous release version branch and adapt as needed (the complicated part). Consider copying the changes related to the objects that HULL deals with and leave other API changes alone. Use a side-by-side tool such as BeyondCompare to do the comparison.

General hints for doing this when starting comparing top to bottom:
- before going through the new `values.schema.json` line by line you should do some global replacements in the new file to adapt the types of objects to the HULL types:
  - ```
    "type": "object"
    --> 
    "anyOf": [
      {
        "$ref": "#/definitions/hull.Transformation.Pattern"
      },
      {
        "type": "object"
      }
    ]
    ```
  - ```
    "type": "array"
    --> 
    "anyOf": [
      {
        "$ref": "#/definitions/hull.Transformation.Pattern"
      },
      {
        "type": "array"
      }
    ]
    ```
  - ```
    "type": "integer"
    --> 
    "anyOf": [
      {
        "$ref": "#/definitions/hull.Transformation.Pattern"
      },
      {
        "type": "integer"
      }
    ]
    ```
  - ```
    "type": "number"
    --> 
    "anyOf": [
      {
        "$ref": "#/definitions/hull.Transformation.Pattern"
      },
      {
        "type": "number"
      }
    ]
    ```
  - ```
    "type": "boolean"
    --> 
    "anyOf": [
      {
        "$ref": "#/definitions/hull.Transformation.Pattern"
      },
      {
        "type": "boolean"
      }
    ]
    ```
  - the `required` properties need to be removed to improve defaulting capabilities. When you have `required` properties you would need to set them on each object instance's fields which defeats the purpose of efficient defaulting via `sources` or `_HULL_OBJECT_TYPE_DEFAULT_`. To remove all required properties the following regex search and replacement can be used. Note that the below syntax is guarenteed to be working with VSCode, it may need to be adapted when using other editors for the regex replacing.
  - ```
    ^(\s+)"required":\s\[(.|\S|\r|\n)*?\]
    -->
    $1"required": []
    ```  

  This should eliminate more than 80% of the differences between current `values.schema.json` and the next one you compare with. The remaining differences are typically the following:
  - description changes
  - added `x-kubernetes` attributes on the Kubernetes side
  - deprecated APIs are removed
  - new APIs are added (see below, this may require updating the HULL structures if the new API is handled by HULL)
  
- any block that ends with `.Names` and before that matches one of the Kubernetes API schema elements (typically right below such a block) you copy the block over to the new JSON schema. These blocks are used in the HULL schema to create valid union between K8S properties and HULL properties. For example this block:

  ```yaml
  "io.k8s.api.apps.v1.StatefulSetSpec.Names": {
      "enum": [
        "podManagementPolicy",
        "replicas",
        "revisionHistoryLimit",
        "updateStrategy",
        "serviceName",
        "volumeClaimTemplates"
      ]
    },
  ```

- `selector` and `template` elements for top level K8S objects need to be removed from the schema. HULL creates these elements automatically under the hood. If `selector` and `template` are listed under `required` elements remove them from the list as well
- remove the `"additionalProperties": false` property from the top-level object schema
- other properties which are part of the merged HULL JSON schema object need to be removed from the Kubernetes object schema, eg. `name`, `env`, `envFrom`, `volumeMounts` and `ports` from the `Container` spec
- keep text-only changes to descriptions in the new schema
- keep properties that are added to objects in the new schema which are not handled explicitly by HULL
- if properties are added to an object which is handled by HULL and has a matching `.Names` block the new property name needs to be added to the `.Names` block
- added `staticName` properties to objects need to be copied over to the new schema
- if a top-level object migrates to a new version, you can create an incremented HULL schema object for the new version and reference it in the schema

### Adapt `Chart.yaml`

Set the versions in `Chart.yaml`:

- `version: 1.x.0` where x is the Kubernetes major version
- `appVersion: 1.x.y` where x is the Kubernetes major version and y the patch version of the schema

### Adapt `templates\_objects.tpl`

In case that API versions of objects have been updated with a new Kubernetes release it is necessary to update the respective `API_VERSION`s in the `_objects.tpl` to reflect the update and keep up to date with the created objects.

For example, when `cronjob` migrated from `v1beta1` to `v1` with Kubernetes 1.21 the line:

`{{- $allObjects = merge $allObjects (dict "CronJob" (dict "API_VERSION" "batch/v1beta1")) }}`

is changed to

`{{- $allObjects = merge $allObjects (dict "CronJob" (dict "API_VERSION" "batch/v1")) }}`

Also make the same change(s) to the per-object type files of `hull` which you may use to render a file per object type instead of one big `hull.yaml`. the files are located in the `files/templates` folder.

### Adapt test schema

Replace the files for the Kubernetes JSON schema in `hull/files/test/HULL/schema` with the created files from the new subfolder of `kubernetes-json-schema`. This makes the JSON validation test against the new version.

### Run tests

All tests need to run successfully.

## Run tests

HULL has a large number of test cases aiming to cover a large amount of usage scenarios. The testing framework in use is [Gauge](https://gauge.org/index.html). To run the tests it is advised to use VisualStudio Code or the `gauge` CLI.

Before any tests can be executed you need to have `Python` and `pip` installed, preferrably in the latest version. Then run `pip install -r requirements.txt` when in the `hull/files/test/HULL` folder. This installs the necessary Python libraries for test execution. 

Now you should be able to run a first test suite, for example on the `job` scenario:

```
gauge run --hide-suggestion --simple-console hull\files\test\HULL\specs\job.spec
```

After the tests have run you can see how many tests failed and were successful. Additionally you will be provided with a link to a local HTML file giving you an overview of all executed test cases.

### Update documentation

Typically it should be enough to replace `/generated/kubernetes-api/v1.x` with `/generated/kubernetes-api/v1.y` where x is the preceding Kubernetes version and y the newly created release version. But also check other places where `1.y` is used if they need updating.

### Update CHANGELOG.md and HISTORY.md

Update the changelog with the information what was changed within the update.
The changelog has just the most recent information, copy this entry over in to the history.

## Creating a new minor version

Creating regular releases for bugfixes and added features requires several actions to be performed. Most of of them are covered already in the Kubernetes release update documentation so these step will not be explained in detail again.

A tried and tested practice for doing minor release updates is this:

- checkout the three latest `fixes-1.x` branches of HULL via `git worktree` so you can do comparisons on a folder level (eg. using BeyondCompare)
- start implementation in the most recent of the `fixes-1.x` branches and make sure everything listed below is done in terms of implementation
- on a folder level, apply same functional changes to other two `fixes-x` branches. **Take care to respect the differences between release branches such as different Kubernetes versions mentioned and sometimes changed APIs!**
- Once all three `fixes-1.x` branches are ready they can be commited.
- Issue PRs in GitHub for all three `fixes-1.x` branches to merge the matching `fixes-1.x` branch to the respective `release-1.x` branch. **When creating the PRs make sure to click "Update Branch" directly so the Gated tests don't need to run twice in case you missed this early on!**
- Once gated Tests and thus PRs are successfully reviewed (the gated tests run against all latest version of each supported Helm minor release), the PRs can be completed. 
- The HULL release creation process itself requires external action by a HULL maintainer with access to the release pipeline! 

  _As a note to people creating releases, sometimes the last stage of publishing the Helm chart fails due to GitHub authentication issues and potentially timing. If so, retrying this failed step a couple of times resolves the problem usually._
- After all three new releases have been successfully created, make sure to mark the release of `hull-demo` in the latest branch in GitHub as the current release. This is to foster download of the demo chart to start local testing of it. Marking the `hull` release itself has no added benefit since in almost all cases you would not download it from GitHub directly but pull it in via `helm dep update`.
- Create closing PR to merge from latest `release-1.x` branch to `main` and complete the PR. This concludes the release process.

Below an overview of the implementation steps is given for a minor release:

### Make the code changes

This typically involves work on files in the `templates` folder and maybe on files in the root folder such as the `values.schema.json` and the `values.yaml`

### Adapt the JSON schema (if needed)

Make the changes required for the version update.

### Adapt tests

Add or modify test cases so that the new changes are covered adequately.

### Run tests

All tests need to run successfully to create a new release.

### Update documentation 

Document the new feature or effects of a bug fix in the respective places. There are two `README.md` which have for the most part identical content (one is embedded in the chart and one represents the git repositories `README.md`) which may require an update. Also the remaining documentation is to be found in the `doc` folder, please check if one of the covered aspects has changed and update the documentation therefore.

### Update CHANGELOG.md and HISTORY.md

Update the changelog with the information what was changed within the update.
The changelog has just the most recent information, copy this entry over in to the history.

### Update Helm Release compatibility

Check whether a new release of Helm has been published since the last release(s). If so, update the pipeline code in `azure-pipelines-gated.yaml` and `azure-pipelines.yaml` to include the new release in the tests. For `azure-pipelines-gated.yaml` it is sufficient to replace the latest minor version with the newly released one since the gated tests run only on the latest minor versions on each supported Helm branch. For `azure-pipelines.yaml` extend the list of Helm versions to test against with the new Helm release version.

---
Back to [README.md](./../README.md)