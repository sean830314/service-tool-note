package internal

import (
	"context"
	"errors"
)

// StringService provides operations on strings.
type IService1 interface {
	Ping(context.Context, string) (string, error)
}

// stringService is a concrete implementation of StringService
type Service1 struct{}

func (Service1) Ping(_ context.Context, s string) (string, error) {
	if s == "" {
		return "", ErrEmpty
	}
	return "Ping " + s, nil
}

// ErrEmpty is returned when an input string is empty.
var ErrEmpty = errors.New("empty string")
