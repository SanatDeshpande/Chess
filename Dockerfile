FROM golang:latest
RUN mkdir /app
RUN mkdir /app/src
RUN mkdir /app/src/main
RUN mkdir /app/src/test
ADD src/main/ /app/src/main
ADD src/test/ /app/src/test
WORKDIR /app
ENV GOPATH=/app
RUN go build -o app main
CMD ["./app"]
