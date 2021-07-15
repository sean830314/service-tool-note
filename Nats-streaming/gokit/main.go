package main

import (
	"flag"
	"log"
	"net/http"

	httptransport "github.com/go-kit/kit/transport/http"
	natstransport "github.com/go-kit/kit/transport/nats"
	"github.com/nats-io/nats.go"
	"github.com/sean830314/service-tool-note/Nats-streaming/gokit/internal"
)

// Transports expose the service to the network. In this fourth example we utilize JSON over NATS and HTTP.
func main() {
	svc := internal.Service1{}

	natsURL := flag.String("nats-url", nats.DefaultURL, "URL for connection to NATS")
	flag.Parse()

	nc, err := nats.Connect(*natsURL)
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()
	pingHTTPHandler := httptransport.NewServer(
		internal.MakePingHTTPEndpoint(nc),
		internal.DecodePingHTTPRequest,
		httptransport.EncodeJSONResponse,
	)

	pingHandler := natstransport.NewSubscriber(
		internal.MakePingEndpoint(svc),
		internal.DecodePingRequest,
		natstransport.EncodeJSONResponse,
	)

	uSub, err := nc.QueueSubscribe("service1.ping", "stringsvc", pingHandler.ServeMsg(nc))
	if err != nil {
		log.Fatal(err)
	}
	defer uSub.Unsubscribe()

	http.Handle("/ping", pingHTTPHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))

}
