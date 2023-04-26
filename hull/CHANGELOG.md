# Changelog
------------------
[1.27.1]
------------------
CHANGES:
- allow to set an explicit namespaceOverride via chart configuration on the object instances rendered. This is helpful for usage with helm template command so that rendered templates contain a namespace and can be used directly in GitOps style declarative workflows. If no namespaceOverride is provided, the namespace is now still always added to the object instances and falls back to the release namespace.