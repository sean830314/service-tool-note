package internal

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/nats-io/nats.go"
)

func DecodePingHTTPRequest(_ context.Context, r *http.Request) (interface{}, error) {
	var request pingRequest
	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		return nil, err
	}
	return request, nil
}

func DecodePingResponse(_ context.Context, msg *nats.Msg) (interface{}, error) {
	var response pingResponse

	if err := json.Unmarshal(msg.Data, &response); err != nil {
		return nil, err
	}

	return response, nil
}

func DecodePingRequest(_ context.Context, msg *nats.Msg) (interface{}, error) {
	var request pingRequest

	if err := json.Unmarshal(msg.Data, &request); err != nil {
		return nil, err
	}
	return request, nil
}
