package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"golang/main/api"
	"golang/main/service"
	"net/http"
	"os"
	"strings"
	"time"
)

var detectionApi = api.DetectionAPI{
	Url:    os.Getenv("DETECTION_API_URL"),
	Client: &http.Client{Timeout: 20 * time.Second}}

var recognitionApi = api.RecognitionAPI{
	Url:    os.Getenv("RECOGNITION_API_URL"),
	Client: &http.Client{Timeout: 20 * time.Second}}

var imageService = service.ImageService{}

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
	requestId := uuid.New().String()
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	file, _, err := r.FormFile("image")
	if err != nil {
		createErrorResponse(w, err.Error(), http.StatusBadRequest)
		return
	}
	img, imgAsBytes, err := imageService.ProcessImage(file)
	if err != nil {
		createErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if !imageService.CheckImageDimensions(img) {
		createErrorResponse(w, "Image dimensions are too large", http.StatusBadRequest)
		return
	}
	boxes, err := detectionApi.GetMinimalTextBoxes(imgAsBytes)
	if err != nil {
		createErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	croppedImages := imageService.CropImage(img, boxes)
	imagesAsBytes := make([][]byte, 0)
	for _, croppedImage := range croppedImages {
		croppedImageAsBytes, err := imageService.ConvertImageToByteArray(croppedImage)
		if err != nil {
			createErrorResponse(w, err.Error(), http.StatusInternalServerError)
			return
		}
		imagesAsBytes = append(imagesAsBytes, croppedImageAsBytes)
	}
	textResponse, err := recognitionApi.ExtractText(imagesAsBytes)
	if err != nil {
		createErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(ReadResponse{Id: requestId, Text: strings.Join(textResponse.Tokens, " ")})
	if err != nil {
		createErrorResponse(w, err.Error(), http.StatusInternalServerError)
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
