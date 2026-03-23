# Changelog

## [1.35.3]

FIXES:

- fixed error handling changes because it caused installation failures with [errors in disabled content](https://github.com/vidispine/hull/issues/401) and [sub chart rendering](https://github.com/vidispine/hull/issues/393). Instead of the changed approach (raising every error that occurs during processing) and the original approach (raise only errors in rendered objects), a combined approach is used now. The old error handling practice is restored (raise all visible errors in templates) but extended with raising errors from `conditionals` references, however this is limited to the cases where the associated object is actually rendered. If errors in `conditional` references are recorded for objects that don't get rendered in the end, the errors are dropped.
- improved error messages for better understanding and added object tree paths for direct identification of error source
