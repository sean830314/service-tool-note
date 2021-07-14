package internal

import (
	"github.com/ThreeDotsLabs/watermill"
	"github.com/ThreeDotsLabs/watermill-amqp/pkg/amqp"
	"github.com/ThreeDotsLabs/watermill-nats/pkg/nats"
	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/ThreeDotsLabs/watermill/pubsub/gochannel"
	stan "github.com/nats-io/stan.go"
)

var marshaler nats.GobMarshaler

// NewGoChannel returns a go channel pubsub
func NewGoChannel(logger watermill.LoggerAdapter) *gochannel.GoChannel {
	return gochannel.NewGoChannel(gochannel.Config{
		// If persistent is set to true, when subscriber subscribes to the topic,
		// it will receive all previously produced messages
		Persistent: true,
	}, logger)
}

// NewNATSPublisher returns a NATS publisher
func NewNATSPublisher(logger watermill.LoggerAdapter, clusterID, natsURL string) (message.Publisher, error) {
	return nats.NewStreamingPublisher(
		nats.StreamingPublisherConfig{
			ClusterID: clusterID,
			ClientID:  watermill.NewShortUUID(),
			StanOptions: []stan.Option{
				stan.NatsURL(natsURL),
			},
			Marshaler: marshaler,
		}, logger)
}

// NewNATSSubscriber returns a NATS subscriber
func NewNATSSubscriber(logger watermill.LoggerAdapter, clusterID, clientID, natsURL string) (message.Subscriber, error) {
	return nats.NewStreamingSubscriber(
		nats.StreamingSubscriberConfig{
			ClusterID: clusterID,
			ClientID:  clientID,
			StanOptions: []stan.Option{
				stan.NatsURL(natsURL),
			},
			Unmarshaler: marshaler,
		},
		logger,
	)
}

// NewAMQPWorkQueuePublisher returns a AMQP publisher
func NewAMQPWorkQueuePublisher(logger watermill.LoggerAdapter, amqpURI string) (message.Publisher, error) {
	return amqp.NewPublisher(
		amqp.NewDurableQueueConfig(amqpURI),
		logger,
	)
}

// NewAMQPWorkQueueSubscriber returns a AMQP subscriber
func NewAMQPWorkQueueSubscriber(logger watermill.LoggerAdapter, clientID string, amqpURI string) (message.Subscriber, error) {
	return amqp.NewSubscriber(
		amqp.NewDurableQueueConfig(amqpURI),
		logger,
	)
}

// NewAMQFanoutPublisher returns a AMQP publisher
func NewAMQFanoutPublisher(logger watermill.LoggerAdapter, amqpURI string) (message.Publisher, error) {
	return amqp.NewPublisher(
		amqp.NewDurablePubSubConfig(amqpURI, nil),
		logger,
	)
}

// NewAMQPFanoutSubscriber returns a AMQP subscriber
func NewAMQPFanoutSubscriber(logger watermill.LoggerAdapter, clientID string, amqpURI string) (message.Subscriber, error) {
	return amqp.NewSubscriber(
		amqp.NewDurablePubSubConfig(amqpURI, amqp.GenerateQueueNameTopicNameWithSuffix(clientID)),
		logger,
	)
}
