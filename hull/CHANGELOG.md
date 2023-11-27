# Changelog
------------------
[1.26.9]
------------------
FIXES:
- fix broken _HULL_OBJECT_TYPE_DEFAULT_ defaulting of CronJobs properties where all values from _HULL_OBJECT_TYPE_DEFAULT_ or sources where not merged to rendered CronJob instances
- fix missing rendering of embedded Job Kubernetes properties in a Cronjobs jobTemplate where any Kubernetes property of an embedded Job was missing from the rendered output