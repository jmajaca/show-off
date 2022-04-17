package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"main/api"
	"main/common"
	"main/service"
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

var queueService = service.NewQueueService(service.ServerConnectionData{
	Username:    os.Getenv("QUEUE_USERNAME"),
	Password:    os.Getenv("QUEUE_PASSWORD"),
	Host:        os.Getenv("QUEUE_HOST"),
	Port:        os.Getenv("QUEUE_PORT"),
	VirtualHost: os.Getenv("QUEUE_VIRTUAL_HOST"),
}, []service.QueueConnectionData{
	{QueueName: os.Getenv("IMAGE_QUEUE_NAME"), Exchange: ""},
	{QueueName: os.Getenv("IMAGE_DATA_QUEUE_NAME"), Exchange: ""},
	{QueueName: os.Getenv("TEXT_CORRECTION_QUEUE_NAME"), Exchange: ""}})

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
		common.CreateErrorResponse(w, err.Error(), http.StatusBadRequest)
		return
	}
	img, imgAsBytes, err := imageService.ProcessImage(file)
	if err != nil {
		common.CreateErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if !imageService.CheckImageDimensions(img) {
		common.CreateErrorResponse(w, "Image dimensions are too large", http.StatusBadRequest)
		return
	}
	queueService.SendImage(requestId, imgAsBytes)
	boxes, err := detectionApi.GetMinimalTextBoxes(imgAsBytes)
	if err != nil {
		common.CreateErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	croppedImages := imageService.CropImage(img, boxes)
	imagesAsBytes := make([][]byte, 0)
	for _, croppedImage := range croppedImages {
		croppedImageAsBytes, err := imageService.ConvertImageToByteArray(croppedImage)
		if err != nil {
			common.CreateErrorResponse(w, err.Error(), http.StatusInternalServerError)
			return
		}
		imagesAsBytes = append(imagesAsBytes, croppedImageAsBytes)
	}
	textResponse, err := recognitionApi.ExtractText(imagesAsBytes)
	if err != nil {
		common.CreateErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	queueService.SendImageData(requestId, boxes, textResponse.Tokens)
	w.Header().Set("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(common.ReadResponse{Id: requestId, Text: strings.Join(textResponse.Tokens, " ")})
	if err != nil {
		common.CreateErrorResponse(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func correctText(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	var request common.TextCorrectionRequest
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		common.CreateErrorResponse(w, err.Error(), http.StatusBadRequest)
		return
	}
	queueService.SendTextCorrection(request)
	w.WriteHeader(http.StatusAccepted)
}

func main() {

	http.HandleFunc("/health", health)
	http.HandleFunc("/read", WrapWithLogs(read))
	http.HandleFunc("/correct-text", WrapWithLogs(correctText))

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		return
	}

}
