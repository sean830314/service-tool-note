# NATS-Streamming

## Local run

run NATS-Streamming
```
docker run -p 4222:4222 -p 8222:8222  nats-streaming:latest
```

run RabbitMQ
```
docker run -p 5672:5672 rabbitmq:3-management
```

WATERMILL in AMQP 
```
WATERMILL_PUBSUB_TYPE=rabbitmq NATS_CLUSTER_ID=test-cluster NATS_URL=nats://localhost:4223 AMQP_URL=amqp://guest:guest@localhost:5672/ go run main.go
```

WATERMILL in NATS-Streamming 
```
WATERMILL_PUBSUB_TYPE=nats NATS_CLUSTER_ID=test-cluster NATS_URL=nats://localhost:4222 go run main.go
```