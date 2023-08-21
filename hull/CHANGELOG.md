# Changelog
------------------
[1.26.5]
------------------
FIXES:
- loosen schema types of image tag, annotation and label values. For image tag values user input of type float or integer and for annotation and label values user input of type float, integer and boolean is allowed. On rendering a late to string conversion is taking place to guarantee the Kubernetes schema is not violated demanding string values. Reasoning behind is that for these fields correct quoting of user input is often missing in case of values which are interpreted as non-strings. Allowing a flexible input type and late guaranteed conversion to string helps avoid unncessary and unexpected errors due to user input.
- drop kubeVersion from Chart.yaml to support running hull-demo in lower version clusters, kubeVersion field does not seem to have relevance for hull as a library chart but is copied over to hull-demo Chart.yaml