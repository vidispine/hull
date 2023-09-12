# Changelog
------------------
[1.28.2]
------------------
FIXES:
- extend loosening of schema type to env fields. User input of type float, integer or boolean is now allowed and on rendering a late to string conversion is taking place to guarantee the Kubernetes schema is not violated demanding string values. 