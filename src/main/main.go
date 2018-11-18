package main


import (
    "log"
    "net/http"
    "fmt"
)

func hanlder(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, r.URL.Path)
}

func main() {
    http.HandleFunc("/", hanlder)
    fmt.Println("Listening on port 8000...")
    log.Fatal(http.ListenAndServe(":8000", nil))
}
