<!-- filepath: /home/georg/git/hull/hull/hull/README.md -->
# HULL: Helm Uniform Layer Library

> Abstractions need to be maintained - Kelsey Hightower

## Introduction

Helm encourages users to create abstractions for Kubernetes application configuration. Each Helm Chart is represented by YAML templates in the `/templates` directory. These templates combine standard Kubernetes YAML with custom configuration logic using Go Templating, connecting the application's settings in `values.yaml` to the final Kubernetes manifests. While this method allows for highly customized deployments, it can introduce complexity and overhead for common use cases. Managing and understanding numerous Helm charts from different sources can become a challenge.

HULL aims to simplify this process by enabling users to define Kubernetes objects directly in `values.yaml`, eliminating the need for custom YAML templates. The HULL library chart acts as a consistent layer for specifying, configuring, and rendering Helm charts. It provides a streamlined approach, letting you bypass the template middleman and work closer to the Kubernetes API. JSON schema validation (via `values.schema.json`) helps ensure your configuration matches Kubernetes standards, especially when using an IDE with live schema validation.

### Versioning

HULL releases are aligned with Kubernetes versions, as each release incorporates the corresponding Kubernetes API schemas. Patch releases for Kubernetes do not affect HULL versioning, while HULL patch releases focus on improvements and fixes for the library itself. Compatibility with Helm is maintained according to Kubernetes support policies.

### Helm v3 vs Helm v4

HULL supports both Helm 3 and Helm 4, starting with versions `1.34.2`, `1.33.3`, and `1.32.6`. Note that Helm 4 introduces some changes:

- Property names in the Helm root context may have different capitalization.
- Unset values are handled differently: Helm 3 treats them as empty strings, while Helm 4 omits them from the object tree, which can cause errors if accessed.

These changes are generally less impactful for HULL-based charts, but it's important to be aware of them.

**Feedback is welcome! Please use the Issues section for questions, feature requests, or bug reports.**

HULL draws inspiration from the [common Helm chart](https://github.com/helm/charts/tree/master/incubator/common) and is tested using [Gauge](https://gauge.org).

[![Gauge Badge](https://gauge.org/Gauge_Badge.svg)](https://gauge.org)

[![Build Status](https://dev.azure.com/arvato-systems-dmm/VPMS3%20CrossCutting/_apis/build/status/vidispine.hull?branchName=main)](https://dev.azure.com/arvato-systems-dmm/VPMS3%20CrossCutting/_build/latest?definitionId=589&branchName=main)

## Quick Start - the `hull-demo` chart

To get started, download the latest `hull-demo` Helm chart from the Releases section. This chart provides a sample application called `myapp` with both `frontend` and `backend` deployments and services. The backend receives a configuration file via a ConfigMap, and the frontend uses environment variables to connect to the backend service. The setup can be switched between debug mode (NodePort service) and production mode (ClusterIP service with ingress) using a central configuration switch.

A basic structure for this configuration might look like:

```yaml
hull: # HULL is configured via subchart key 'hull'
  config: # chart setup takes place here for everything besides object definitions
```

After downloading the chart, run:

```bash
helm template hull-demo-<version>.tgz
```

This will render Kubernetes objects based on the provided `values.yaml`, including:

- A deployment for `myapp-frontend` with a configurable image tag and environment variables for backend service discovery.

- A deployment for `myapp-backend` with a configurable image tag and a mounted configuration file from a ConfigMap.

- A `myappconfig` ConfigMap containing a JSON file built from templating expressions and cross-references in `values.yaml`.

- A ClusterIP Service for the backend deployment.

- A frontend service whose type and port depend on the debug switch—either NodePort or ClusterIP with ingress.

- An ingress object for `myapp`, created only if `debug: false` is set.

All these aspects can be adjusted using overlay `values.yaml` files, such as:

- Switching between debug and production modes.
- Adding resource definitions.
- Setting ingress hostname and path.
- Adding environment variables.
- Modifying or replacing ConfigMap contents.

This demo uses less than a hundred lines of configuration in `values.yaml`. You can experiment by adding overlays or use it as a starting point for your own chart.

## Key Features Overview

HULL provides several benefits when included in a Helm chart:

### No YAML templates required

You can specify Kubernetes objects directly, without writing custom templates. This reduces errors and maintenance. HULL validates rendered output against the Kubernetes API schema.

  For more details, see [JSON Schema Validation](/hull/files/doc/json_schema_validation.md).

### Full access to Kubernetes object properties

All supported object types can be configured completely. Chart maintainers don't need to add missing options one by one, and users don't need to fork charts for extra properties. Updating HULL to match new Kubernetes API versions is all that's needed.

  For more details, see [Architecture Overview](/hull/files/doc/architecture.md).

### Unified configuration interface with schema validation

HULL uses a single interface for object creation and configuration, backed by JSON schema validation. IDEs with live validation help prevent misconfiguration.

  For more details, see [JSON Schema Validation](/hull/files/doc/json_schema_validation.md).

### Automatic metadata enrichment

All objects created by HULL receive consistent metadata. Advanced examples show how to override metadata as needed.

### Flexible ConfigMap and Secret integration

ConfigMap and Secret data can be specified inline or imported from files. File contents can be templated or used as-is, and HULL handles serialization and encoding automatically.

  For more details, see [ConfigMaps and Secrets](/hull/files/doc/API/hull_objects_configmaps_secrets.md).

### Advanced defaulting to reduce repetition

Defaults can be set for object fields, labels, annotations, environment variables, and volumes, minimizing repeated configuration.

  For more details, see [Chart Design](/hull/files/doc/chart_design.md).

### Go Templating in `values.yaml`

Complex scenarios can be handled by injecting Go Templating expressions directly in `values.yaml`, allowing dynamic value calculation and cross-referencing.

  For more details, see [Transformations](/hull/files/doc/transformations.md).

### Optional hashing for ConfigMaps and Secrets

Enable hashing to trigger pod restarts when configuration changes.

  For more details, see [Pods](/hull/files/doc/API/hull_objects_pod.md).

For more on HULL's architecture and features, see the [Architecture Overview](/hull/files/doc/architecture.md).

## Important information

⚠️ **HULL is a non-breaking addition to your Helm charts. You can use it alongside traditional templates, choosing the best approach for each part of your chart.** ⚠️
