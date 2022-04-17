package main

import (
	"fmt"
	"github.com/google/uuid"
	"log"
	"net/http"
	"strconv"
	"time"
)

var incomingMsg = "Incoming Request: %s, %s - \"%s %s %s\""
var outgoingMsg = "Outgoing Response: %s, Duration %s ms, %s %d - Body: %s"

func WrapWithLogs(handler http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		id := uuid.New().String()
		start := time.Now()
		uri := r.RequestURI
		method := r.Method
		host := r.Host
		protocol := r.Proto

		log.Println(fmt.Sprintf(incomingMsg, id, host, method, uri, protocol))

		responseData := &ResponseData{}

		lrw := LoggingResponseWriter{
			ResponseWriter: w,
			responseData:   responseData,
		}

		handler.ServeHTTP(&lrw, r)

		duration := time.Since(start)

		log.Println(fmt.Sprintf(outgoingMsg, id, strconv.FormatInt(duration.Milliseconds(), 10), protocol, responseData.status, responseData.body))
	}
}

type ResponseData struct {
	status int
	body   string
}

type LoggingResponseWriter struct {
	http.ResponseWriter
	responseData *ResponseData
}

func (w *LoggingResponseWriter) Write(b []byte) (int, error) {
	size, err := w.ResponseWriter.Write(b)
	w.responseData.body = string(b)
	return size, err
}

func (w *LoggingResponseWriter) WriteHeader(statusCode int) {
	w.responseData.status = statusCode
	w.ResponseWriter.WriteHeader(statusCode)
}
