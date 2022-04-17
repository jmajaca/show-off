package service

type ImageBoxData struct {
	StartX int    `json:"start_x"`
	StartY int    `json:"start_y"`
	Width  int    `json:"width"`
	Height int    `json:"height"`
	Text   string `json:"text"`
}

type ImageBoxDataList []ImageBoxData

type TextCorrection struct {
	Id   string `json:"id"`
	Text string `json:"text"`
}

type ServerConnectionData struct {
	Username    string
	Password    string
	Host        string
	Port        string
	VirtualHost string
}

type QueueConnectionData struct {
	QueueName string
	Exchange  string
}
