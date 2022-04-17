package common

import (
	"encoding/json"
	"net/http"
	"time"
)

func CreateErrorResponse(w http.ResponseWriter, description string, statusCode int) {
	w.Header().Set("Content-Type", "application/json")
	body := ErrorResponse{Error: description, Timestamp: time.Now()}
	err := json.NewEncoder(w).Encode(body)
	if err != nil {
		return
	}
	w.WriteHeader(statusCode)
}
