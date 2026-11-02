# Import

Convert Kubernetes manifests into HULL values with hull/files/scripts/hull_import.py and verify
that the converted chart renders the same objects as the input.

## Typical classic chart output is converted exactly
* Import manifests "classic-chart.yaml" for release "shop" in namespace "demo" and verify the round trip
* The import report has a note for "Pod/shop-web-test-connection" containing "imported as generic object"
* The imported values contain "noObjectNamePrefixes: true"
* The imported values contain "      shop-web:"

## Conversions needing special care are exact
* Import manifests "edge-cases.yaml" for release "rel" in namespace "demo" and verify the round trip
* The import report has a note for "Service/external-db" containing "a Service without selector gets a default selector in HULL, imported as generic object"
* The import report has a note for "Ingress/static" containing "imported as generic object"
* The import report has a note for "Deployment/web" containing "unnamed port 8080 of container sidecar gets the name tcp-8080-2"
* The import report has a note for "Deployment/web" containing "has a tag and a digest, HULL renders it by digest only"
* The imported values contain "assignDefaultServiceAccountToPods: false"
* The imported values contain "noTemplating: true"
* The imported values contain "preEncoded: true"
* The imported values contain "metadataNameOverride: web"
