# Changelog
------------------
[1.27.13]
------------------
FIXES:
- fixed `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` not existing in context of `_HT?` boolean transformations. Access to `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` is now provided same as in context of `_HT!` and `_HT/` transformations
- fixed inability to use `OBJECT_INSTANCE_KEY` and `OBJECT_TYPE` for `_HULL_OBJECT_TYPE_DEFAULT_` instances in context of `_HT/` include transformations. This fix allows to combine `postRender` replacements in content created by `_HT/` transformations on a `_HULL_OBJECT_TYPE_DEFAULT_` instance