# Captain's log :wheel_of_dharma:
A metrics exporter for Kubernetes events. In this project we assume that events older than default 5 seconds is old news and we will discard them.

It requires a Kubernetes config file to consume events and for local development you will need Python 3.8 and pipenv installed.

To get started run:

```bash
# Run locally
make install # install dependencies

cp .env.example .env # creating environment variables file

make run # run the service
```

## Running in Kubernetes
See k8s-example/ folder for example manifests for Kubernetes. Assuming you have Prometheus deployed already it will collect metrics based on the service annotations specified.

```bash
kubectl apply -f k8s-example/ # applying manifest to Kubernetes
```

## Configuration
Currently this project only supports a few optional configurations via environment variables.

This project can be configured in two main ways:

1) in-cluster configuration using pod serviceaccount (no KUBECONFIG environment variable specified)
2) outside-cluster configuration using kube config file (KUBECONFIG environment variable set to e.g. "$HOME/.kube/config"). This is mainly relevant for development.

| Environment variable | Description | Example |
|---|---|---|
| PORT | Port for serving metrics **OPTIONAL** | 8080 |
| OFFSET | Offset (in seconds) used to discard old events **OPTIONAL** | 5 |
| KUBECONFIG | Absolute path for kube config file **OPTIONAL** | "$HOME/.kube/config" |