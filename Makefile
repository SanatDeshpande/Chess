all:
	env GOPATH=$(PWD) go build -o app main
clean:
	rm app
