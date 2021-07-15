package internal

import (
	"fmt"

	"github.com/ThreeDotsLabs/watermill"
	"github.com/ThreeDotsLabs/watermill/message"
)

type OrderHandler struct{}

type RestaurantHandler struct{}

type PaymentHandler struct{}

// Handler receives the published message and publish to my_outgoing topic
// if there is error in this handler or router fails to publish to my_outgoing, the msg will be NACKed
func (h OrderHandler) Handler(msg *message.Message) ([]*message.Message, error) {
	fmt.Printf(
		"\n> OrderHandler received message: %s\n> %s\n> metadata: %v\n",
		msg.UUID, string(msg.Payload), msg.Metadata,
	)

	msg = message.NewMessage(watermill.NewUUID(), []byte("greet from OrderHandler"))
	return message.Messages{msg}, nil
}

// HandlerWithoutPublish receives and handles subscribe message without publishing it again
func (h RestaurantHandler) HandlerWithoutPublish(msg *message.Message) error {
	fmt.Printf(
		"\n> RestaurantHandler received message: %s\n> %s\n> metadata: %v\n",
		msg.UUID, string(msg.Payload), msg.Metadata,
	)
	return nil
}

// HandlerWithoutPublish receives and handles subscribe message without publishing it again
func (h PaymentHandler) HandlerWithoutPublish(msg *message.Message) error {
	fmt.Printf(
		"\n> PaymentHandler received message: %s\n> %s\n> metadata: %v\n",
		msg.UUID, string(msg.Payload), msg.Metadata,
	)
	return nil
}
