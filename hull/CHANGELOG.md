# Changelog

## [1.36.1]

CHANGES:

- added `pod.annotations` and `pod.labels` as the preferred place to specify pod template metadata for workload objects, since this metadata ends up on the pod. The existing object instance level `templateAnnotations` and `templateLabels` keys are an equivalent alternative and remain fully supported. Both are merged and where the same key is defined in both, the `pod` level value wins.
- added control over the order of array elements that HULL renders from dictionaries. Previously, array elements were always rendered in alphanumeric order of their dictionary keys which is problematic where Kubernetes attaches meaning to the order. The elements of `containers`, `initContainers`, `volumes`, `env`, `envFrom`, `ports`, `volumeMounts`, service `ports`, ingress `rules`, `paths` and `tls`, role `rules`, `webhooks` and all Gateway API dictionaries now support an integer `order` property (default `0`) by which they are sorted ascending before alphanumeric key order applies. Additionally, `env` variables are automatically rendered after the variables of the same container they reference via `$(VAR_NAME)` in their `value`, making [dependent environment variables](https://github.com/vidispine/hull/issues/414) work out of the box. Without `order` properties and forward references in `env` values the rendered order is unchanged. See the [chart design guide](/hull/files/doc/chart_design.md#ordering-of-array-elements) for details.
- added the previously missing `enabled` property to the JSON schema of all Gateway API array elements that HULL renders from dictionaries. The `enabled` property of GRPCRoute and HTTPRoute `backendRefs` elements is now also evaluated on rendering.
- added the `hull.config.general.assignDefaultServiceAccountToPods` switch (default `true`). Pods without an explicit `serviceAccountName` are assigned the `default` ServiceAccount as before; set the switch to `false` to opt out of this assignment while still rendering the `default` ServiceAccount.
- container `sources` are now applied before `containers` and `initContainers` are ordered, so the `order` property can be provided via container `sources` too. Same as with object instance `sources`, the `enabled` property of pod and container `sources` is not inherited.

FIXES:

- fixed Gateway `listeners` silently dropping `tls` and `allowedRoutes` whenever they had exactly one key, for example `tls` with only `certificateRefs` or `frontendValidation`, or `allowedRoutes` with only `namespaces` or `kinds`.
