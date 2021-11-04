------------------
[1.20.12]
------------------

CHANGES:
- add CHANGELOG.md
- add ingressclass objects as main objects
- allow to specify rules in roles key-value based instead of as an array (array also supported)
- add unit tests for ClusterRole and ClusterRoleBindings

FIXES: 
- clusterrole and clusterrolebinding objects with enabled=false or nulled were rendering incorrectly as empty objects 
- cronjob pods must not have selector set

------------------
[1.20.11]
------------------
FEATURES: 
- allow enabled property on all key-value pair HULL objects
- allow to use string as input for enabled property in order to use HULL transformations on enabled properties