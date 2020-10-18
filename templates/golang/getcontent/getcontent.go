package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

func main() {

	sURL := "https://api.covidtracking.com/v1/states/current.json"
	response, err := http.Get(sURL)
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
		defer response.Body.Close()
		contents, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Printf("%s", err)
			os.Exit(1)
		} else {				
			// Declared an empty interface of type Array
			var results []map[string]interface{}

			// Unmarshal or Decode the JSON to the interface.
			json.Unmarshal([]byte(contents), &results)

			for key, result := range results {			
				//Reading each value by its key
				fmt.Println(key, "State :", result["state"], result["positive"])
			}
		}	
	}
}

