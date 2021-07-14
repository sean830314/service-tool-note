package main

// WATERMILL_PUBSUB_TYPE=rabbitmq NATS_CLUSTER_ID=test-cluster NATS_URL=nats://localhost:4223 AMQP_URL=amqp://guest:guest@localhost:5672/ go run main.go
// WATERMILL_PUBSUB_TYPE=nats NATS_CLUSTER_ID=test-cluster NATS_URL=nats://localhost:4223 go run main.go
import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/ThreeDotsLabs/watermill"
	"github.com/ThreeDotsLabs/watermill/components/metrics"
	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/ThreeDotsLabs/watermill/message/router/middleware"
	"github.com/ThreeDotsLabs/watermill/message/router/plugin"
	"github.com/sean830314/service-tool-note/Nats-streaming/internal"
)

var (
	metricsAddr         = ":8081"
	watermillPubsubType = os.Getenv("WATERMILL_PUBSUB_TYPE")
	natsClusterID       = os.Getenv("NATS_CLUSTER_ID")
	natsURL             = os.Getenv("NATS_URL")
	amqpURL             = os.Getenv("AMQP_URL")
	// You probably want to ship your own implementation of `watermill.LoggerAdapter`.
	logger         = watermill.NewStdLogger(false, false) // debug=false, trace=false
	orderChannel   = "order_channel"
	paymentChannel = "payment_channel"
)

func main() {
	router, err := message.NewRouter(message.RouterConfig{}, logger)
	if err != nil {
		log.Fatal(err)
	}

	promRegistry, closeMetricsServer := metrics.CreateRegistryAndServeHTTP(metricsAddr)
	defer closeMetricsServer()

	metricsBuilder := metrics.NewPrometheusMetricsBuilder(promRegistry, "demo", "hello")
	metricsBuilder.AddPrometheusRouterMetrics(router)

	// SignalsHandler gracefully shutdowns Router when receiving SIGTERM
	router.AddPlugin(plugin.SignalsHandler)

	// Router level middleware are executed for every message sent to the router
	router.AddMiddleware(
		// CorrelationID will copy the correlation id from the incoming message's metadata to the produced messages
		middleware.CorrelationID,
		// Timeout makes the handler cancel the incoming message's context after a specified time
		middleware.Timeout(time.Second*10),
		// Throttle provides a middleware that limits the amount of messages processed per unit of time
		middleware.NewThrottle(10, time.Second).Middleware,
		// After MaxRetries, the message is Nacked and it's up to the PubSub to resend it
		middleware.Retry{
			MaxRetries: 5,
			Logger:     logger,
		}.Middleware,

		// Recoverer handles panics from handlers
		middleware.Recoverer,
	)

	var publisher message.Publisher
	var subscriber message.Subscriber
	if watermillPubsubType == "nats" {
		publisher, err = internal.NewNATSPublisher(logger, natsClusterID, natsURL)
		if err != nil {
			log.Fatal(err)
		}
		subscriber, err = internal.NewNATSSubscriber(logger, natsClusterID, watermill.NewShortUUID(), natsURL)
		if err != nil {
			log.Fatal(err)
		}
	} else if watermillPubsubType == "rabbitmq" {
		fmt.Println("in rabbitmq ======")
		publisher, err = internal.NewAMQFanoutPublisher(logger, amqpURL)
		if err != nil {
			log.Fatal(err)
		}
		subscriber, err = internal.NewAMQPFanoutSubscriber(logger, watermill.NewShortUUID(), amqpURL)
		if err != nil {
			log.Fatal(err)
		}

	} else {
		pubsub := internal.NewGoChannel(logger)
		publisher = pubsub
		subscriber = pubsub
	}

	// // Handler AMQP fanout
	// subscriber2, err := internal.NewAMQPFanoutSubscriber(logger, watermill.NewShortUUID(), amqpURL)
	// if err != nil {
	// 	log.Fatal(err)
	// }

	// // Handler AMQP fanout
	// handler := router.AddHandler(
	// 	orderChannel+"_handler",         // Handler name, must be unique
	// 	orderChannel,                    // Topic from which we will read events
	// 	subscriber2,                     // Subscriber (which we should subscribe from)
	// 	paymentChannel,                  // Topic to which we will publish events
	// 	publisher,                       // Publisher (which we should publish to)
	// 	internal.OrderHandler{}.Handler, // How we process the message from subscriber and send to publisher
	// )

	// Handler subsribes a topic and publishes other messages when it receives a message
	handler := router.AddHandler(
		"order_handler",                 // Handler name, must be unique
		orderChannel,                    // Topic from which we will read events
		subscriber,                      // Subscriber (which we should subscribe from)
		paymentChannel,                  // Topic to which we will publish events
		publisher,                       // Publisher (which we should publish to)
		internal.OrderHandler{}.Handler, // How we process the message from subscriber and send to publisher
	)

	// Handler level middleware is only executed for a specific handler
	// Such middleware can be added the same way the router level ones
	handler.AddMiddleware(func(h message.HandlerFunc) message.HandlerFunc {
		return func(message *message.Message) ([]*message.Message, error) {
			fmt.Printf("\nexecuting order_handler specific middleware for %s", message.UUID)
			return h(message)
		}
	})

	// This handler cannot return messages, just receiving messages
	// We are printing all messages received on `incoming_messages_topic`
	router.AddNoPublisherHandler(
		"restaurant_handler",
		orderChannel,
		subscriber,
		internal.RestaurantHandler{}.HandlerWithoutPublish,
	)

	// We are printing all events sent to `outgoing_messages_topic`
	router.AddNoPublisherHandler(
		paymentChannel+"_handler",
		paymentChannel,
		subscriber,
		internal.PaymentHandler{}.HandlerWithoutPublish,
	)

	// Producing some incoming messages in background
	go publishMessages(orderChannel, publisher)

	// Run the router
	ctx := context.Background()
	if err := router.Run(ctx); err != nil {
		log.Fatal(err)
	}
}

func publishMessages(topic string, publisher message.Publisher) {
	for {
		msg := message.NewMessage(watermill.NewUUID(), []byte("Hello, watermill!"))
		middleware.SetCorrelationID(watermill.NewUUID(), msg)

		fmt.Printf("\n\n\nSending message %s, correlation id: %s\n", msg.UUID, middleware.MessageCorrelationID(msg))
		if err := publisher.Publish(topic, msg); err != nil {
			log.Fatal(err)
		}
		time.Sleep(10 * time.Second)
	}
}
