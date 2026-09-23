# Changelog

## [1.37.0]

CHANGES:

- initial K8S 1.37 release
- deprecating 1.34 release
- BREAKING: the `default` ServiceAccount, `default` Role and `default` RoleBinding are not created automatically anymore. Previously they were rendered for every release unless a global pod `serviceAccountName` was configured under `hull.config.templates.pod.global`, and pods without an explicit `serviceAccountName` were wired to the `default` ServiceAccount. Creation is now opt-in via the new `hull.config.general.createDefaultRbacTriplet` switch which defaults to `false`, set it to `true` to restore the previous behavior.
- added `pod.annotations` and `pod.labels` as the preferred place to specify pod template metadata for workload objects, since this metadata ends up on the pod. The existing object instance level `templateAnnotations` and `templateLabels` keys are an equivalent alternative and remain fully supported. Both are merged and where the same key is defined in both, the `pod` level value wins.
