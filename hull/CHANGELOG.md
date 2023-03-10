# Changelog
------------------
[1.26.2]
------------------
CHANGES:
- by adding property hashsumAnnotation: true to a pods volumeMount, env or envFrom referencing a ConfigMap or Secret, a pod restart can be enforced in case of changed contents. This works by calculation of a hashsum of the contents and adding it to the pods template annotations. This is recommended practice as documented in the [Helm documentation](https://helm.sh/docs/howto/charts_tips_and_tricks/#automatically-roll-deployments) in order to handle applications that require restarts on certain configuration changes.