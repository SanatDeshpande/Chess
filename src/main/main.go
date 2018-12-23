package main


import (
    "log"
    "net/http"
    "fmt"
)


func main() {
    http.Handle("/", http.FileServer(http.Dir("./static")))

    fmt.Printf("Listening on port 8000...")
    log.Fatal(http.ListenAndServe(":8000", nil))
}
