package internal

import (
	"context"
	"fmt"

	"github.com/go-kit/kit/endpoint"
	natstransport "github.com/go-kit/kit/transport/nats"
	"github.com/nats-io/nats.go"
)

// For each method, we define request and response structs
type pingRequest struct {
	S string `json:"s"`
}

type pingResponse struct {
	V   string `json:"v"`
	Err string `json:"err,omitempty"` // errors don't define JSON marshaling
}

// Endpoints are a primary abstraction in go-kit. An endpoint represents a single RPC (method in our service interface)
func MakePingHTTPEndpoint(nc *nats.Conn) endpoint.Endpoint {
	return natstransport.NewPublisher(
		nc,
		"service1.ping",
		natstransport.EncodeJSONRequest,
		DecodePingResponse,
	).Endpoint()
}

func MakePingEndpoint(svc IService1) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		fmt.Println("start consume Ping task")
		req := request.(pingRequest)
		v, err := svc.Ping(ctx, req.S)
		if err != nil {
			return pingResponse{v, err.Error()}, nil
		}
		return pingResponse{v, ""}, nil
	}
}
