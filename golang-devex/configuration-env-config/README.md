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

The code to access the environemnt config is as follows.

```go
env, ok := request.GetContextKey(req, "apiextensions.crossplane.io/environment")
if !ok {
    f.log.Info("Environment config not obtained")
} else {
    f.log.Info("Environment config", "info", env)
}
```
