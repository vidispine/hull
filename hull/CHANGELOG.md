# Changelog
------------------
[1.29.4]
------------------
FIXES:
- fixed problem with running both HULL transformations and `tpl` on `path` content in ConfigMaps and Secrets. After loading the external files content, decide whether to run HULL transformations or `tpl` based on HULL transformation prefix presence
- fixed checks for `virtualFolderDataPathExists` and `virtualFolderDataInlineValid` in the case of Secrets. Due to the Base64 encoding of data any error signaling strings weren't properly detected. With added Base64 decoding of the content for secrets the error checks now work for both ConfigMaps and Secrets
- make all keys within `.Values` available for reference in Secret and ConfigMap `data` `inline` and `path` content templating. Due to obsolete code, all other keys than `hull` were removed from the parent charts `.Values` context when being passed to ConfigMap and Secret for template processing. Thanks again [khmarochos](https://github.com/khmarochos) for pointing out the problem [in this isue](https://github.com/vidispine/hull/issues/288)