# icap-argo

## Pre-requisits 
- Docker Desktop
- Kubernetes Enabled

## Installing Octant
Octant can be used as an easy way to manage the kubernetes environment.

To install run:
```
choco install octant --confirm
```

To run: 
```
octant
```

## Setup

### Create Namespace

```
kubectl create ns argo-events
```

### Install Rabbit MQ to the Namespace

```
kubectl create -n argo-events -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-service.yaml
```
```
kubectl create -n argo-events -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-controller.yaml
```

### Installing Argo Workflow

```
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/quick-start-postgres.yaml
```

To enable the Argo Workflow UI, you need to port forward on port 2746

```
kubectl -n argo-events port-forward deployment/argo-server 2746:2746
```

### Installing Argo Events

```
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
```
```
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/eventbus/native.yaml
```

### Setting up the AMQP Event

Expose the RabbitMQ port if needed

```
kubectl -n argo-events port-forward <rabbitmq-pod-name> 5672:5672
```

Create the event source
```
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/event-sources/amqp.yaml
```

Create the sensor
```
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/sensors/amqp.yaml
```

