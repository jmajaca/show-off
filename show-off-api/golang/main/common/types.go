package common

import "time"

type ErrorResponse struct {
	Error     string    `json:"error"`
	Timestamp time.Time `json:"timestamp"`
}

type ReadResponse struct {
	Id   string `json:"id"`
	Text string `json:"text"`
}

type TextCorrectionRequest struct {
	Id   string `json:"id"`
	Text string `json:"text"`
}
