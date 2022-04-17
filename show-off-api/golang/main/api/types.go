package api

type MinimalTextBox struct {
	StartX int `json:"start_x"`
	StartY int `json:"start_y"`
	Width  int `json:"width"`
	Height int `json:"height"`
}

type MinimalTextBoxes []MinimalTextBox

type RecognitionResponse struct {
	Tokens []string `json:"tokens"`
}
