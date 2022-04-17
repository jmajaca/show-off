package api

import (
	"bytes"
	"encoding/json"
	"mime/multipart"
	"net/http"
)

func post(client *http.Client, url string, payload *bytes.Buffer, target interface{}, headers map[string]string) (int, error) {
	request, err := http.NewRequest(http.MethodPost, url, payload)
	if err != nil {
		return 0, err
	}
	for key, value := range headers {
		request.Header.Set(key, value)
	}
	response, err := client.Do(request)
	if err != nil {
		return 0, err
	}
	err = json.NewDecoder(response.Body).Decode(target)
	if err != nil {
		return 0, err
	}
	err = response.Body.Close()
	if err != nil {
		return 0, err
	}
	return response.StatusCode, nil
}

func get(client *http.Client, url string, target interface{}, headers map[string]string) (int, error) {
	request, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return 0, err
	}
	for key, value := range headers {
		request.Header.Set(key, value)
	}
	response, err := client.Do(request)
	if err != nil {
		return 0, err
	}
	err = json.NewDecoder(response.Body).Decode(target)
	if err != nil {
		return 0, err
	}
	err = response.Body.Close()
	if err != nil {
		return 0, err
	}
	return response.StatusCode, nil
}

func packImageFilesToMultipartFormRequest(data map[string][]byte) (*bytes.Buffer, string, error) {
	buffer := new(bytes.Buffer)
	bodyWriter := multipart.NewWriter(buffer)
	for key, value := range data {
		fileWriter, err := bodyWriter.CreateFormFile(key, key+".jpg")
		if err != nil {
			return nil, "", err
		}
		_, err = fileWriter.Write(value)
		if err != nil {
			return nil, "", err
		}
	}
	err := bodyWriter.Close()
	if err != nil {
		return nil, "", err
	}
	return buffer, bodyWriter.FormDataContentType(), nil
}
