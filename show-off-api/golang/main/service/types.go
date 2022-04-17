package service

type ImageBoxData struct {
	StartX int    `bson:"start_x"`
	StartY int    `bson:"start_y"`
	Width  int    `bson:"width"`
	Height int    `bson:"height"`
	Text   string `bson:"text"`
}

type ImageBoxDataList []ImageBoxData

type TextCorrection struct {
	Id   string `bson:"id"`
	Text string `bson:"text"`
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
