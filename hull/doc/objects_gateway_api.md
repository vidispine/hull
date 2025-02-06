# Working with the Gateway API 

The Gateway API has been currently implemented in version 1.2.0-experimental.

## JSON Schema Elements

### The `hull.BackendLBPolicy.v1alpha2` properties

Properties can be set as they are defined in the [Kubernetes API's BackendLBPolicy spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.BackendLBPolicy). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `targetRefs` | Dictionary with TargetRefs to add to the BackendLBPolicy's `targetRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1alpha2.LocalPolicyTargetReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.LocalPolicyTargetReference) properties. | `{}` || `{}` 

### The `hull.BackendTLSPolicy.v1alpha2` properties

Properties can be set as they are defined in the [Kubernetes API's BackendTLSPolicy spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha3.BackendTLSPolicy). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `targetRefs` | Dictionary with TargetRefs to add to the BackendTLSPolicy's `targetRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1alpha3.LocalPolicyTargetReferenceWithSectionName`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.LocalPolicyTargetReferenceWithSectionName) properties. | `{}` || `{}` 

### The `hull.Gateway.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.GatewayAddress` are converted to an array on rendering

> The key-value pairs of value type `https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.Listener` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's Gateway spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.Gateway). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `addresses` | Dictionary with GatewayAddresses to add to the Gateway's `addresses` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GatewayAddress`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewayAddress) properties.  | `{}` || `{}` 
| `listeners` | Dictionary with Listeners to add to the Gateway's `listeners` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.Listener`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.Listener) properties except<br> `allowedRoutes.kinds` property of type **`hull.RouteGroupKind.v1`** and <br>`tls.certificateRefs` property of type **`hull.SecretObjectReference.v1`** and <br>`tls.frontendValidation.caCertificateRefs` property of type **`hull.ObjectReference.v1`**.<br>See below for additional types. | `{}` || `{}` 

### The `hull.RouteGroupKind.v1` properties under `gateway.networking.k8s.io/v1.AllowedRoutes`

> The key-value pairs of value type `hull.RouteGroupKind.v1` are converted to an array on rendering

Properties can be set as they are defined in the elements [Kubernetes API's AllowedRoutes spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.AllowedRoutes). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `kinds` | Dictionary with Kinds to add to the AllowedRoutes's `kinds` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.RouteGroupKind`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.RouteGroupKind) properties. | `{}` || `{}` 

### The `hull.SecretObjectReference.v1` properties under `gateway.networking.k8s.io/v1.GatewayTLSConfig`

> The key-value pairs of value type `hull.SecretObjectReference.v1` are converted to an array on rendering

Properties can be set as they are defined in the elements [Kubernetes API's GatewayTLSConfig spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GatewayTLSConfig). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `certificateRefs` | Dictionary with CertificateRefs to add to the GatewayTLSConfig's `certificateRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io/v1.SecretObjectReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.SecretObjectReference) properties. | `{}` || `{}` 

### The `hull.ObjectReference.v11` properties under `gateway.networking.k8s.io/v1.FrontendTLSValidation`

> The key-value pairs of value type `hull.ObjectReference.v1` are converted to an array on rendering

Properties can be set as they are defined in the elements [Kubernetes API's FrontendTLSValidation spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.FrontendTLSValidation). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `caCertificateRefs` | Dictionary with CaCertificateRefs to add to the FrontendTLSValidation's `caCertificateRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ObjectReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ObjectReference) properties. | `{}` || `{}` 

### The `hull.ReferenceGrant.v1beta1` properties

> The key-value pairs of value type `gateway.networking.k8s.io/v1beta1.ReferenceGrantTo` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io/v1beta1.ReferenceGrantFrom` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's ReferenceGrant spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1beta1.ReferenceGrant). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `from` | Dictionary with ReferenceGrantFroms to add to the ReferenceGrant's `from` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io/v1beta1.ReferenceGrantFrom`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1beta1.ReferenceGrantFrom) properties. | `{}` || `{}` 
| `to` | Dictionary with ReferenceGrantTos to add to the ReferenceGrant's `to` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io/v1beta1.ReferenceGrantTo`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1beta1.ReferenceGrantTo) properties. | `{}` || `{}` 

### The `hull.GRPCRoute.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.ParentReference` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io.v1.GRPCRouteRule` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's GRPCRoute spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCRoute). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `parentRefs` | Dictionary with ParentReferences to add to the GRPCRoute's `parentRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ParentReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties. | `{}` || `{}`
| `rules` | Dictionary with Rules to add to the GRPCRoute's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GRPCRouteRule`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties and  **`hull.GRPCRouteRule.v1`** properties (see below). | `{}` || `{}`

### The `hull.GRPCRouteRule.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io/v1.GRPCRouteFilter` are converted to an array on rendering 

> The key-value pairs of value type `gateway.networking.k8s.io/v1.GRPCBackendRef` are converted to an array on rendering 

> The key-value pairs of value type `gateway.networking.k8s.io/v1.GRPCRouteMatch` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's GRPCRouteRoule spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCRouteRule). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `filters` | Dictionary with GRPCRouteFilter to add to the GRPCRoute's `filters` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GRPCRouteFilter`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCRouteFilter) properties. | `{}` || `{}`
| `matches` | Dictionary with GRPCRouteMatch to add to the GRPCRoute's `matches` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GRPCRouteMatch`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCRouteMatch) properties. | `{}` || `{}`
| `backendRefs` | Dictionary with GRPCBackendRefs to add to the GRPCRoute's `backendRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GRPCBackendRef`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCBackendRef) properties and  **`hull.GRPCBackendRef.v1`** properties (see below). | `{}` || `{}`

### The `hull.GRPCBackendRef.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io/v1.GRPCRouteFilter` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's GRPCBackendRef spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCBackendRef). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `filters` | Dictionary with GRPCRouteFilter to add to the GRPCBackendRef's `filters` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.GRPCRouteFilter`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.GRPCRouteFilter) properties. | `{}` || `{}`

### The `hull.TCPRoute.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.ParentReference` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io.v1alpha2.TCPRouteRule` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's TCPRoute spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TCPRoute). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `parentRefs` | Dictionary with ParentReferences to add to the TCPRoute's `parentRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ParentReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties. | `{}` || `{}`
| `rules` | Dictionary with Rules to add to the TCPRoute's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1alpha2.TCPRouteRule`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TCPRouteRule) properties and  **`hull.TCPRouteRule.v1alpha2`** properties (see below). | `{}` || `{}`

### The `hull.TCPRouteRule.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.BackendRef` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's TCPRouteRoule spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TCPRouteRule). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `backendRefs` | Dictionary with BackendRefs to add to the TCPRoute's `backendRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.BackendRef`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.BackendRef) properties. | `{}` || `{}`

### The `hull.TLSRoute.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.ParentReference` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io.v1alpha2.TLSRouteRule` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's TLSRoute spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TLSRoute). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `parentRefs` | Dictionary with ParentReferences to add to the TLSRoute's `parentRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ParentReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties. | `{}` || `{}`
| `rules` | Dictionary with Rules to add to the TLSRoute's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1alpha2.TLSRouteRule`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TCPRouteRule) properties and  **`hull.TLSRouteRule.v1alpha2`** properties (see below). | `{}` || `{}`

### The `hull.TLSRouteRule.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.BackendRef` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's TLSRouteRoule spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TLSRouteRule). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `backendRefs` | Dictionary with BackendRefs to add to the TCPRoute's `backendRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.BackendRef`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.BackendRef) properties. | `{}` || `{}`

### The `hull.UDPRoute.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.ParentReference` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io.v1alpha2.UDPRouteRule` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's UDPRoute spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.UDPRoute). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `parentRefs` | Dictionary with ParentReferences to add to the UDPRoute's `parentRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ParentReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties. | `{}` || `{}`
| `rules` | Dictionary with Rules to add to the UDPRoute's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1alpha2.UDPRouteRule`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.TCPRouteRule) properties and  **`hull.UDPRouteRule.v1alpha2`** properties (see below). | `{}` || `{}`

### The `hull.UDPRouteRule.v1alpha2` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.BackendRef` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's UDPRouteRoule spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1alpha2.UDPRouteRule). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `backendRefs` | Dictionary with BackendRefs to add to the UDPRoute's `backendRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.BackendRef`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.BackendRef) properties. | `{}` || `{}`

### The `hull.HTTPRoute.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io.v1.ParentReference` are converted to an array on rendering

> The key-value pairs of value type `gateway.networking.k8s.io.v1.HTTPRouteRule` are converted to an array on rendering

Properties can be set as they are defined in the [Kubernetes API's HTTPRoute spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPRoute). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `parentRefs` | Dictionary with ParentReferences to add to the HTTPRoute's `parentRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.ParentReference`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties. | `{}` || `{}`
| `rules` | Dictionary with Rules to add to the HTTPRoute's `rules` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.HTTPRouteRule`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.ParentReference) properties and  **`hull.HTTPRouteRule.v1`** properties (see below). | `{}` || `{}`

### The `hull.HTTPRouteRule.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io/v1.HTTPRouteFilter` are converted to an array on rendering 

> The key-value pairs of value type `gateway.networking.k8s.io/v1.HTTPBackendRef` are converted to an array on rendering 

> The key-value pairs of value type `gateway.networking.k8s.io/v1.HTTPRouteMatch` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's HTTPRouteRoule spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPRouteRule). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `filters` | Dictionary with HTTPRouteFilter to add to the HTTPRoute's `filters` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.HTTPRouteFilter`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPRouteFilter) properties. | `{}` || `{}`
| `matches` | Dictionary with HTTPRouteMatch to add to the HTTPRoute's `matches` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.HTTPRouteMatch`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPRouteMatch) properties. | `{}` || `{}`
| `backendRefs` | Dictionary with HTTPBackendRefs to add to the HTTPRoute's `backendRefs` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.HTTPBackendRef`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPBackendRef) properties and  **`hull.HTTPBackendRef.v1`** properties (see below). | `{}` || `{}`

### The `hull.HTTPBackendRef.v1` properties

> The key-value pairs of value type `gateway.networking.k8s.io/v1.HTTPRouteFilter` are converted to an array on rendering 

Properties can be set as they are defined in the [Kubernetes API's HTTPBackendRef spec](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPBackendRef). 

However the properties listed below are overwritten or added by HULL:

| Parameter | Description  | Default | Example 
| --------  | -------------| ------- | --------
| `filters` | Dictionary with HTTPRouteFilter to add to the HTTPBackendRef's `filters` section. <br><br>Key: <br>Unique related to parent element.<br><br>Value: <br>The [**`gateway.networking.k8s.io.v1.HTTPRouteFilter`**](https://gateway-api.sigs.k8s.io/reference/spec/#gateway.networking.k8s.io/v1.HTTPRouteFilter) properties. | `{}` || `{}`


## Overview of HULL based properties

The below tree is from `values.yaml` and indicates which properties are treated as dictionaries on the HULL input side and are rendered as arrays in the output:

```
# GATEWAY API - BACKENDLBPOLICY
  backendlbpolicy:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      targetRefs:
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      
##################################################

# GATEWAY API - BACKENDTLSPOLICY
  backendtlspolicy:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      targetRefs:
        _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - GATEWAYCLASS
  gatewayclass:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
##################################################

# GATEWAY API - GATEWAY
  gateway:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      addresses: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      listeners:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          tls:
            certificateRefs:
              _HULL_OBJECT_TYPE_DEFAULT_: {}
            frontendValidation:
              caCertificateRefs:
                _HULL_OBJECT_TYPE_DEFAULT_: {}
          allowedRoutes:
            kinds:
              _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - GRPCROUTE
  grpcroute:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      parentRefs: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      rules:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          matches:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
          filters:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
          backendRefs:
            _HULL_OBJECT_TYPE_DEFAULT_:
              filters:
                _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - REFERENCEGRANT
  referencegrant:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      from: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      to:
        _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - TCPROUTE
  tcproute:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      parentRefs: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      rules:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          backendRefs:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - TLSROUTE
  tlsroute:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      parentRefs: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      rules:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          backendRefs:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - UDPROUTE
  udproute:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      parentRefs: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      rules:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          backendRefs:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
##################################################

# GATEWAY API - HTTPROUTE
  httproute:
    _HULL_OBJECT_TYPE_DEFAULT_:
      enabled: true
      annotations: {}
      labels: {}
      parentRefs: 
        _HULL_OBJECT_TYPE_DEFAULT_: {}
      rules:
        _HULL_OBJECT_TYPE_DEFAULT_: 
          matches:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
          filters:
            _HULL_OBJECT_TYPE_DEFAULT_: {}
          backendRefs:
            _HULL_OBJECT_TYPE_DEFAULT_:
              filters:
                _HULL_OBJECT_TYPE_DEFAULT_: {}
```

---
Back to [README.md](./../README.md)