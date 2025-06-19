# Example for Obtaining Environment Config From Golang Embedded Function

Login to your Upbound account.
Build and deploy this project.
Switch context to your dev control plane.
Apply a resouce claim.
Examine the logs with the environment config.

```shell
up login
up project run
up ctx ./configuration-env-config
kubectl apply -f examples/environment-config-example.yaml
kubectl -n crossplane-system logs $(k -n crossplane-system get pods | grep upbound-configuration-env-configcompose|awk '{print $1}')
```

Below is the environment config that we have applied.

```yaml
apiVersion: apiextensions.crossplane.io/v1beta1
kind: EnvironmentConfig
metadata:
  name: example-config
data:
  locations:
    us: us-east-2
    eu: eu-north-1
  key1: value1
  key2: value2
  key3:
    - item1
    - item2
```

With the above environment config, a sample log output looks like below.

```shell
{"level":"info","ts":1750371870.7922056,"caller":"compose/fn.go:21","msg":"Running function","tag":"dceba39fc77fe2c6f732d700a5f50679238fa30acdb8171a90a568dd9655f065"}
{"level":"info","ts":1750371870.7923763,"caller":"compose/fn.go:29","msg":"Environment config","info":"struct_value:{fields:{key:\"apiVersion\"  value:{string_value:\"internal.crossplane.io/v1alpha1\"}}  fields:{key:\"key1\"  value:{string_value:\"value1\"}}  fields:{key:\"key2\"  value:{string_value:\"value2\"}}  fields:{key:\"key3\"  value:{list_value:{values:{string_value:\"item1\"}  values:{string_value:\"item2\"}}}}  fields:{key:\"kind\"  value:{string_value:\"Environment\"}}  fields:{key:\"locations\"  value:{struct_value:{fields:{key:\"eu\"  value:{string_value:\"eu-north-1\"}}  fields:{key:\"us\"  value:{string_value:\"us-east-2\"}}}}}}"}
```

The code to access the environemnt config is as follows.

```go
env, ok := request.GetContextKey(req, "apiextensions.crossplane.io/environment")
if !ok {
    f.log.Info("Environment config not obtained")
} else {
    f.log.Info("Environment config", "info", env)
}
```
