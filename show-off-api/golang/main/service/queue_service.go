package service

import (
	"encoding/json"
	"github.com/streadway/amqp"
	"golang/main/api"
	"golang/main/common"
	"log"
	"os"
)

type QueueService struct {
	Channel *amqp.Channel
	Queues  map[string]QueueConnectionData
}

func NewQueueService(server ServerConnectionData, queues []QueueConnectionData) *QueueService {
	service := new(QueueService)
	connectionString := "amqp://" + server.Username + ":" + server.Password + "@" + server.Host + ":" + server.Port + "/" + server.VirtualHost
	connection, err := amqp.Dial(connectionString)
	if err != nil {
		panic(err)
	}
	channel, err := connection.Channel()
	if err != nil {
		panic(err)
	}
	queueMap := make(map[string]QueueConnectionData, 0)
	for _, queueData := range queues {
		_, err := channel.QueueDeclare(
			queueData.QueueName,
			true,
			false,
			false,
			false,
			nil,
		)
		if err != nil {
			panic(err)
		}
		queueMap[queueData.QueueName] = queueData
	}
	service.Channel = channel
	service.Queues = queueMap
	return service
}

func (service QueueService) SendImage(requestId string, image []byte) {
	queue := service.Queues[os.Getenv("IMAGE_QUEUE_NAME")]
	err := service.sendDataToQueue(queue, requestId, image, "application/octet-stream")
	failOnError(err, "Did not send data to imageQueue")
}

func (service QueueService) SendImageData(requestId string, boxes api.MinimalTextBoxes, tokens []string) {
	data := ImageBoxDataList{}
	if len(tokens) != len(boxes) {
		return
	}
	for i := range boxes {
		data = append(data, ImageBoxData{
			StartX: boxes[i].StartX,
			StartY: boxes[i].StartY,
			Width:  boxes[i].Width,
			Height: boxes[i].Height,
			Text:   tokens[i],
		})
	}
	queue := service.Queues[os.Getenv("IMAGE_DATA_QUEUE_NAME")]
	err := service.sendDataToQueue(queue, requestId, data, "application/json")
	failOnError(err, "Did not send data to imageDataQueue")
}

func (service QueueService) SendTextCorrection(inputRequest common.TextCorrectionRequest) {
	request := TextCorrection{Id: inputRequest.Id, Text: inputRequest.Text}
	queue := service.Queues[os.Getenv("TEXT_CORRECTION_QUEUE_NAME")]
	err := service.sendDataToQueue(queue, request.Id, request, "application/json")
	failOnError(err, "Did not send data to TextCorrectionQueue")
}

func (service QueueService) sendDataToQueue(queue QueueConnectionData, requestId string, payload interface{}, contentType string) error {
	byteRequest, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	return service.Channel.Publish(
		queue.Exchange,
		queue.QueueName,
		false,
		false,
		amqp.Publishing{
			ContentType: contentType,
			Headers:     map[string]interface{}{"request_id": requestId},
			Body:        byteRequest,
		})
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}
