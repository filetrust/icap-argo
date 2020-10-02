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

## Running a file

To run a file through the workflow, you will first need to upload the file to minio and then send a rabbitmq message with the filename to process.

### Forwarding ports

Forward minio
```
kubectl -n argo-events port-forward services/argo-artifacts 9000:9000
```

Forward Argo Workflow UI
```
kubectl -n argo-events port-forward deployment/argo-server 2746:2746
```

Forward RabbitMQ 
```
kubectl -n argo-events port-forward <rabbitmq pod name> 5672:5672
```

### Uploading file to minio
Go to localhost:9000. Sign in with the default Access Key & Secret:

- AccessKey: AKIAIOSFODNN7EXAMPLE
- SecretKey: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

Create 2 buckets 'glasswalltarget' & 'glasswallsource'. Within 'glasswallsource' there needs to be an additional folder named 'matt' inside that folder upload the file you want processed

### Sending a message to the queue
Running the following python script will send a message to the rabbitmq to be picked up by the rebuild workflow. 

Make sure you have pika installed first.

```
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='adaptation-exchange',
                      routing_key='adaptation-request',
                      body='{"sourceFile": "<NAME OF FILE>"}')
```

### Viewing the workflow
Go to locahost:2746 to see the workflow processing