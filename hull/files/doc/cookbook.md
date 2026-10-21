# Cookbook

Recipes for common tasks, each a complete `hull` section of a chart's `values.yaml` with a short explanation of what HULL makes of it. The test suite renders every recipe exactly as written here and checks the result, so they are known to work with the HULL version this page belongs to.

In the explanations, objects are named the way HULL names them: `<release>-<chart>-<key>`, for example `my-release-shop-web` for the key `web` of a chart `shop` installed as `my-release`. Check your own variations with [`hull_validate.py`](/hull/files/doc/error_codes.md#checking-a-chart-with-hull_validatepy) or `helm template`.

| Recipe | Shows |
| ------ | ----- |
| [Web application](#web-application) | Deployment, Service and Ingress with TLS, shared values |
| [Configuration with automatic restarts](#configuration-with-automatic-restarts) | ConfigMap from structured values, restart on change |
| [Settings shared by many containers](#settings-shared-by-many-containers) | `_HULL_OBJECT_TYPE_DEFAULT_` |
| [Database migration as Helm hook](#database-migration-as-helm-hook) | Hook Job, credentials from a Secret |
| [Pinning images by digest](#pinning-images-by-digest) | `digest`, a central registry |
| [Optional components](#optional-components) | `enabled` with `_HT?` |
| [ServiceAccount with permissions](#serviceaccount-with-permissions) | ServiceAccount, Role, RoleBinding, `_HT^` |
| [Database with persistent storage](#database-with-persistent-storage) | StatefulSet, headless Service, volume claims |
| [Scheduled job](#scheduled-job) | CronJob |
| [Restricting traffic to a workload](#restricting-traffic-to-a-workload) | NetworkPolicy with `_HT&` |
| [Init containers in a fixed order](#init-containers-in-a-fixed-order) | `order` |
| [Using objects that are not part of the chart](#using-objects-that-are-not-part-of-the-chart) | `staticName` |

## Web application

A Deployment with a Service in front and an Ingress with TLS. The image tag and the host name are kept once in `hull.config.specific` and referenced where they are needed.

<!-- recipe: web-application -->
```yaml
hull:
  config:
    specific:
      version: "2.3.0"
      host: shop.example.com
  objects:
    deployment:
      web:
        replicas: 2
        pod:
          containers:
            main:
              image:
                repository: example/shop-web
                tag: _HT*hull.config.specific.version
              ports:
                http:
                  containerPort: 8080
              readinessProbe:
                httpGet:
                  path: /ready
                  port: http
    service:
      web:
        ports:
          http:
            port: 80
            targetPort: http
    ingress:
      web:
        ingressClassName: nginx
        annotations:
          cert-manager.io/cluster-issuer: letsencrypt
        tls:
          web:
            hosts: _HT![ {{ _HT*hull.config.specific.host }} ]
            secretName: web-tls
        rules:
          shop:
            host: _HT*hull.config.specific.host
            http:
              paths:
                root:
                  path: /
                  pathType: Prefix
                  backend:
                    service:
                      name: web
                      port:
                        name: http
```

- The Service has no `selector`: HULL generates one that selects the pods of the Deployment with the same key, `web`.
- The Ingress refers to the Service and to the TLS Secret by key. HULL renders the full names `<release>-<chart>-web` and `<release>-<chart>-web-tls`, so cert-manager creates the Secret under that name.
- Changing `version` updates the image of every container that references it.
- `hosts` is a list, so the host is put into a list with `_HT![ ... ]`, which embeds the `_HT*` reference in a template. A transformation written as an element of a list does not work here: if the first element of a list is a transformation, its result replaces the whole list, and further elements are not transformed.

## Configuration with automatic restarts

A ConfigMap built from values, mounted into the pods, which are restarted when the configuration changes.

<!-- recipe: configuration-restart -->
```yaml
hull:
  config:
    specific:
      log_level: info
  objects:
    configmap:
      settings:
        data:
          app.yaml:
            inline:
              logLevel: _HT*hull.config.specific.log_level
              search:
                enabled: true
          nginx.conf:
            inline: |
              server {
                listen 8080;
              }
    deployment:
      web:
        pod:
          containers:
            main:
              image:
                repository: example/shop-web
                tag: "2.3.0"
              volumeMounts:
                settings:
                  name: settings
                  mountPath: /etc/shop
                  hashsumAnnotation: true
          volumes:
            settings:
              configMap:
                name: settings
```

- `inline` content that is a dictionary is serialized according to the file extension of the key, YAML for `app.yaml`, JSON for `.json` keys. Plain strings are taken as they are.
- `hashsumAnnotation: true` on the mount adds an annotation with the hash of each data key of the mounted ConfigMap to the pod template. When the content changes, the pod template changes and Kubernetes rolls the pods.
- Content for `data` can also come from files of the chart with `path: files/nginx.conf` instead of `inline`. Add `noTemplating: true` to content that contains `{{` not meant for Helm.

## Settings shared by many containers

Settings that apply to all containers of all Deployments of the chart, defined once.

<!-- recipe: shared-container-settings -->
```yaml
hull:
  objects:
    deployment:
      _HULL_OBJECT_TYPE_DEFAULT_:
        pod:
          containers:
            _HULL_OBJECT_TYPE_DEFAULT_:
              resources:
                requests:
                  cpu: 100m
                  memory: 128Mi
              securityContext:
                allowPrivilegeEscalation: false
                readOnlyRootFilesystem: true
      api:
        pod:
          containers:
            main:
              image:
                repository: example/shop-api
                tag: "2.3.0"
      worker:
        pod:
          containers:
            main:
              image:
                repository: example/shop-worker
                tag: "2.3.0"
              resources:
                requests:
                  cpu: 500m
```

- `_HULL_OBJECT_TYPE_DEFAULT_` below an object type applies to all its instances, inside a dictionary such as `containers` it applies to all elements.
- Values given for an instance are merged on top of the defaults: the `worker` container requests `500m` CPU and keeps the default memory request.
- For defaults that only some objects should get, define instances with `enabled: false` and list them in the `sources` of the objects that use them, see [chart design](/hull/files/doc/chart_design.md).

## Database migration as Helm hook

A Job that migrates the database before the application is installed or upgraded, with the password from a Secret of the chart.

<!-- recipe: migration-hook -->
```yaml
hull:
  config:
    specific:
      database:
        host: postgres.example.com
        password: change-me
  objects:
    secret:
      database:
        annotations:
          helm.sh/hook: pre-install,pre-upgrade
          helm.sh/hook-weight: "-1"
          helm.sh/hook-delete-policy: before-hook-creation
        data:
          password:
            inline: _HT*hull.config.specific.database.password
    job:
      migrate:
        annotations:
          helm.sh/hook: pre-install,pre-upgrade
          helm.sh/hook-weight: "0"
          helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
        backoffLimit: 2
        pod:
          restartPolicy: Never
          containers:
            migrate:
              image:
                repository: example/shop-migrate
                tag: "2.3.0"
              env:
                DATABASE_HOST:
                  value: _HT*hull.config.specific.database.host
                DATABASE_PASSWORD:
                  valueFrom:
                    secretKeyRef:
                      name: database
                      key: password
```

- Hooks run before the release's regular objects exist, so the Secret is a hook too, with a lower weight than the Job. With equal weights Helm orders hooks by name and the Job could start before its Secret exists.
- Secret data is written as plain text, HULL encodes it. The `secretKeyRef` refers to the Secret by key and is rendered with its full name.
- The Job's annotations are also rendered on its pod template, where Helm ignores them.

## Pinning images by digest

Images pulled by an immutable digest instead of a tag, all from one registry.

<!-- recipe: digest-pinning -->
```yaml
hull:
  config:
    general:
      globalImageRegistryServer: registry.example.com
    specific:
      digests:
        web: sha256:1ff6c18fbef2045af6b9c16bf034cc421a29027b800e4f9b68ae9b1cb3e9ae07
  objects:
    deployment:
      web:
        pod:
          containers:
            main:
              image:
                repository: example/shop-web
                tag: "2.3.0"
                digest: _HT*hull.config.specific.digests.web
```

- A non-empty `digest` replaces the tag, the image is `registry.example.com/example/shop-web@sha256:1ff6...`. Kubernetes pulls by digest when a reference has both, so the tag would not matter anyway. Keeping it in the values documents the version.
- An empty `digest` falls back to the tag, so the digests can be set per environment.
- `globalImageRegistryServer` puts all images of the chart behind one registry, for example a mirror.

## Optional components

Objects that are only created when a switch in the values is on.

<!-- recipe: optional-components -->
```yaml
hull:
  config:
    specific:
      search: true
      monitoring: false
  objects:
    deployment:
      search:
        enabled: _HT?(index . "$").Values.hull.config.specific.search
        pod:
          containers:
            main:
              image:
                repository: example/shop-search
                tag: "2.3.0"
    servicemonitor:
      search:
        enabled: _HT?(index . "$").Values.hull.config.specific.monitoring
        selector:
          matchLabels: _HT&search
        endpoints:
        - port: http
```

- `enabled` accepts a boolean or a transformation that results in one. `_HT?` evaluates its argument as a condition, without `{{ }}`.
- With `monitoring: false` the ServiceMonitor is not rendered. Elements of dictionaries, such as a single container or environment variable, can be switched the same way.
- `_HT&search` gives the selector labels HULL generates for the key `search`, which the Service and pods of `search` carry.

## ServiceAccount with permissions

A ServiceAccount for a Deployment with the permission to read ConfigMaps.

<!-- recipe: service-account-rbac -->
```yaml
hull:
  objects:
    serviceaccount:
      app: {}
    role:
      app:
        rules:
          read-config:
            apiGroups: [""]
            resources: [configmaps]
            verbs: [get, list, watch]
    rolebinding:
      app:
        roleRef:
          apiGroup: rbac.authorization.k8s.io
          kind: Role
          name: _HT^app
        subjects:
        - kind: ServiceAccount
          name: _HT^app
          namespace: _HT**Release.Namespace
    deployment:
      app:
        pod:
          serviceAccountName: _HT^app
          containers:
            main:
              image:
                repository: example/shop-app
                tag: "2.3.0"
```

- `serviceAccountName` and the names in RoleBindings are rendered as written, `_HT^app` turns the key into the full name `<release>-<chart>-app`. `_HT**Release.Namespace` is the release namespace.
- The keys of Role `rules` only identify the rules, a plain list of rules works too.
- HULL does not create a `default` ServiceAccount, Role and RoleBinding unless `hull.config.general.createDefaultRbacTriplet` is `true`.

## Database with persistent storage

A StatefulSet with a volume per replica and the headless Service it needs.

<!-- recipe: stateful-database -->
```yaml
hull:
  objects:
    statefulset:
      db:
        serviceName: _HT^db
        replicas: 1
        pod:
          containers:
            postgres:
              image:
                repository: postgres
                tag: "16"
              ports:
                postgres:
                  containerPort: 5432
              volumeMounts:
                data:
                  name: data
                  mountPath: /var/lib/postgresql/data
        volumeClaimTemplates:
        - metadata:
            name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 10Gi
    service:
      db:
        clusterIP: None
        ports:
          postgres:
            port: 5432
            targetPort: postgres
```

- `serviceName` is rendered as written, `_HT^db` gives the full name of the Service `db`, which selects the StatefulSet's pods because both have the key `db`.
- `volumeClaimTemplates` is a plain Kubernetes list, the claims are named after the template, `data`.

## Scheduled job

A CronJob that runs a cleanup every night.

<!-- recipe: scheduled-job -->
```yaml
hull:
  objects:
    cronjob:
      cleanup:
        schedule: "0 3 * * *"
        concurrencyPolicy: Forbid
        job:
          backoffLimit: 1
          pod:
            restartPolicy: OnFailure
            containers:
              cleanup:
                image:
                  repository: example/shop-tools
                  tag: "2.3.0"
                args: [cleanup, --older-than=7d]
```

- The fields of the CronJob's `spec` are written below the instance key, those of its job template's `spec` below `job`, and the pod below `job.pod`.

## Restricting traffic to a workload

A NetworkPolicy that only lets the ingress controller reach the pods of a Deployment.

<!-- recipe: network-policy -->
```yaml
hull:
  objects:
    deployment:
      web:
        pod:
          containers:
            main:
              image:
                repository: example/shop-web
                tag: "2.3.0"
              ports:
                http:
                  containerPort: 8080
    networkpolicy:
      web:
        podSelector:
          matchLabels: _HT&web
        policyTypes: [Ingress]
        ingress:
        - from:
          - namespaceSelector:
              matchLabels:
                kubernetes.io/metadata.name: ingress-nginx
          ports:
          - port: 8080
```

- `_HT&web` gives exactly the labels of the selector HULL generates for the Deployment `web`, so the policy keeps matching its pods when the chart or release name changes.

## Init containers in a fixed order

Init containers that wait for the database and then migrate the schema, in this order.

<!-- recipe: init-container-order -->
```yaml
hull:
  objects:
    deployment:
      web:
        pod:
          initContainers:
            wait-for-database:
              order: 1
              image:
                repository: busybox
                tag: "1.36"
              command: [sh, -c, "until nc -z postgres 5432; do sleep 2; done"]
            migrate-schema:
              order: 2
              image:
                repository: example/shop-migrate
                tag: "2.3.0"
          containers:
            main:
              image:
                repository: example/shop-web
                tag: "2.3.0"
```

- Dictionary elements are rendered in the alphanumeric order of their keys, which would run `migrate-schema` first. `order` sorts them explicitly, lower values first.

## Using objects that are not part of the chart

A Deployment that uses a ConfigMap, a Secret and a certificate Secret managed outside the chart.

<!-- recipe: external-objects -->
```yaml
hull:
  objects:
    deployment:
      web:
        pod:
          containers:
            main:
              image:
                repository: example/shop-web
                tag: "2.3.0"
              envFrom:
                platform-settings:
                  configMapRef:
                    name: platform-settings
                    staticName: true
              env:
                API_TOKEN:
                  valueFrom:
                    secretKeyRef:
                      name: shared-api-token
                      key: token
                      staticName: true
              volumeMounts:
                certificates:
                  name: certificates
                  mountPath: /etc/ssl/company
          volumes:
            certificates:
              secret:
                secretName: company-ca
                staticName: true
```

- References to ConfigMaps, Secrets and other objects are treated as keys of the chart's objects and get the name prefix. `staticName: true` next to the name uses it as written.

---
Back to [README.md](/README.md)
