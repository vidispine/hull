# Changelog
------------------
[1.30.4]
------------------
FIXES:
- fixed unwanted fields being merged when using the `sources` feature. When adding multiple sources, the intermediate results were not only merged into the target object but were also added to the sources themselves permanently. If `_HULL_OBJECT_TYPE_DEFAULT_` is in the sources list, this could lead to unwanted fields merged back into object instances that did not have sources specified and only inherited from `_HULL_OBJECT_TYPE_DEFAULT_` implicitly.