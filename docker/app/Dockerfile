FROM golang:1.10-alpine3.7

RUN apk update && \
    apk add --update git

RUN mkdir -p /go/src/app
WORKDIR /go/src/app

RUN go get github.com/gin-gonic/gin
