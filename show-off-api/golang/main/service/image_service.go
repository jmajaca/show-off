package service

import (
	"bytes"
	"golang/main/api"
	"image"
	"image/jpeg"
	"mime/multipart"
)

type ImageService struct {
}

func (service ImageService) ProcessImage(file multipart.File) (image.Image, []byte, error) {
	img, _, err := image.Decode(file)
	if err != nil {
		return nil, nil, err
	}
	imgAsBytes, err := service.ConvertImageToByteArray(img)
	if err != nil {
		return nil, nil, err
	}
	return img, imgAsBytes, nil
}

func (service ImageService) CheckImageDimensions(img image.Image) bool {
	bounds := img.Bounds()
	width := bounds.Dx()
	height := bounds.Dy()
	return !(width > 1000 || height > 1000)
}

func (service ImageService) CropImage(img image.Image, boxes api.MinimalTextBoxes) []image.Image {
	result := make([]image.Image, 0)
	for _, box := range boxes {
		result = append(result, cropImage(img, box.StartX, box.StartY, box.Width, box.Height))
	}
	return result
}

func (service ImageService) ConvertImageToByteArray(img image.Image) ([]byte, error) {
	buffer := new(bytes.Buffer)
	err := jpeg.Encode(buffer, img, nil)
	if err != nil {
		return nil, err
	}
	return buffer.Bytes(), err
}

func cropImage(img image.Image, x int, y int, width int, height int) image.Image {
	return img.(interface {
		SubImage(r image.Rectangle) image.Image
	}).SubImage(image.Rect(x, y, x+width, y+height))
}
