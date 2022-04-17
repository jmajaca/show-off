package api

import (
	"fmt"
	"net/http"
)

type DetectionAPI struct {
	Url    string
	Client *http.Client
}

func (api DetectionAPI) GetMinimalTextBoxes(img []byte) (MinimalTextBoxes, error) {
	result := MinimalTextBoxes{}
	requestBody, contentType, err := packImageFilesToMultipartFormRequest(map[string][]byte{"image": img})
	if err != nil {
		return nil, err
	}
	headers := map[string]string{"Content-Type": contentType}
	responseCode, err := post(api.Client, api.Url+"/minimal-boxes", requestBody, &result, headers)
	if responseCode != http.StatusOK {
		return nil, fmt.Errorf("detection API responded with status %d", responseCode)
	}
	return result, nil
}
