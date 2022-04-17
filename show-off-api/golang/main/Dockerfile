FROM golang:1.17-alpine

WORKDIR /usr/local/go/src/main

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . ./

RUN go build -o /show-off-api

EXPOSE 8080

ENTRYPOINT ./show-off-api