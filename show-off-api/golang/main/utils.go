package main

import (
	"bytes"
	"encoding/json"
	"image"
	"image/jpeg"
	"net/http"
	"time"
)

func createErrorResponse(w http.ResponseWriter, err error, statusCode int) {
	w.WriteHeader(statusCode)
	w.Header().Set("Content-Type", "application/json")
	body := ErrorResponse{Error: err.Error(), Timestamp: time.Now()}
	err = json.NewEncoder(w).Encode(body)
	if err != nil {
		return
	}
}

func convertImageToByteArray(img image.Image) ([]byte, error) {
	buffer := new(bytes.Buffer)
	err := jpeg.Encode(buffer, img, nil)
	if err != nil {
		return nil, err
	}
	return buffer.Bytes(), err
}
