package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
	"os"
)

func SayHello(w http.ResponseWriter, r *http.Request) {
	_, err := fmt.Fprintf(w, "Hello World")
	if err != nil {
		return
	}
}

func GetItems(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")
	b, err := os.ReadFile("[jsonfile]") // just pass the file name
	if err != nil {
		fmt.Print(err)
	}

	contents := string(b) // convert content to a 'string'
	fmt.Fprintf(w, contents)
}

func GetFilteredItems(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")
	vars := mux.Vars(r)

	b, err := os.ReadFile("[jsonfile]") // just pass the file name
	if err != nil {
		fmt.Print(err)
	}

	contents := string(b) // convert content to a 'string'
	var results map[string]any

	// Unmarshal or Decode the JSON to the interface.
	json.Unmarshal([]byte(contents), &results)

	var aFiltered []interface{}
	wps := results["weapons"].([]interface{})
	for _, wp := range wps {
		//Reading each value by its key
		val := wp.(map[string]any)
		if vars["key"] == val["type"] {
			mFiltered := make(map[string]interface{})
			mFiltered["name"] = val["name"]
			mFiltered["attack"] = val["weight"]
			aFiltered = append(aFiltered, mFiltered)
		}
	}

	jout, _ := json.Marshal(aFiltered)
	sjout := "{\"" + vars["key"] + "\":" + string(jout) + "}"

	fmt.Fprintf(w, sjout)
}

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/", SayHello).Methods("GET")
	r.HandleFunc("/items", GetItems).Methods("GET")
	r.HandleFunc("/items/{key}", GetFilteredItems).Methods("GET")

	err := http.ListenAndServe(":3000", r)
	if err != nil {
		return
	}
}
