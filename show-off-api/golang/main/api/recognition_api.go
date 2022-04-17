package api

import (
	"fmt"
	"net/http"
)

type RecognitionAPI struct {
	Url    string
	Client *http.Client
}

func (api RecognitionAPI) ExtractText(images [][]byte) (RecognitionResponse, error) {
	result := RecognitionResponse{}
	data := make(map[string][]byte, 0)
	for index, value := range images {
		data["image"+string(rune(index))] = value
	}
	requestBody, contentType, err := packImageFilesToMultipartFormRequest(data)
	if err != nil {
		return RecognitionResponse{}, err
	}
	headers := map[string]string{"Content-Type": contentType}
	responseCode, err := post(api.Client, api.Url+"/extract", requestBody, &result, headers)
	if responseCode != http.StatusOK {
		return RecognitionResponse{}, fmt.Errorf("recognition API responded with status %d", responseCode)
	}
	return result, nil
}
