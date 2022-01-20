------------------
[1.22.14]
------------------
CHANGES:
- allow to choose between rendering to single file or multiple files per object type to potentially eliminate performance penalty due to having one file only
- add test environments for both single and multi file usage
- add two example values.yamls

FIXES:
- allow using 63 instead of 54 chars for a fullname and name override
- remove dots end of labels and names

[1.22.13]
------------------
FIXES:
- changed probe port schema to anyOf to avoid clash when using oneOf transformation or string

------------------
[1.22.12]
------------------
FIXES:
- allow mixed transform only when dictionary is returned from transformation and other keys exist besides transformation trigger

------------------
[1.22.11]
------------------
CHANGES:
- added tests for get transformation results
- make every object field subjectable to string transformations irrelevant of input type by large scale extension of JSON schema

FIXES:
- using a get transformation to poulate Configmap/Secret contents produced bad 
character sequences

------------------
[1.22.10]
------------------
CHANGES:
- added short forms for transformations
- documentation improved

------------------
[1.22.9]
------------------
CHANGES:
- fix enabled properties allowed on policyrules in roles, envfrom and tls in ingresses
- allow shorter form of (index . "$") to access parent context

------------------
[1.22.8]
------------------

CHANGES:
- add hull.util.transformation.bool transformation

- BREAKING! change fields for registry population to overwrite any explicit registry fields 

------------------
[1.22.7]
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
[1.22.6]
------------------
CHANGES: 
- allow enabled property on all key-value pair HULL objects
- allow to use string as input for enabled property in order to use HULL transformations on enabled properties