package main

import (
	"encoding/json"
	"golang/main/api"
	"image"
	"net/http"
	"os"
	"time"
)

var detectionApi = api.DetectionAPI{
	Url:    os.Getenv("DETECTION_API_URL"),
	Client: &http.Client{Timeout: 20 * time.Second}}

func health(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	_, err := w.Write([]byte("Health UP"))
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func read(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	file, _, err := r.FormFile("image")
	if err != nil {
		createErrorResponse(w, err, http.StatusBadRequest)
		return
	}
	img, _, err := image.Decode(file)
	if err != nil {
		createErrorResponse(w, err, http.StatusInternalServerError)
		return
	}
	imgAsBytes, err := convertImageToByteArray(img)
	if err != nil {
		createErrorResponse(w, err, http.StatusInternalServerError)
		return
	}
	boxes, err := detectionApi.GetMinimalTextBoxes(imgAsBytes)
	if err != nil {
		createErrorResponse(w, err, http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(boxes)
	if err != nil {
		createErrorResponse(w, err, http.StatusInternalServerError)
		return
	}
}

func main() {

	http.HandleFunc("/health", health)
	http.HandleFunc("/read", read)

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		return
	}

}
