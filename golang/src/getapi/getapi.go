package main

import (
    "fmt"
	  "net/http"
    "io/ioutil"
	  // "encoding/json"
    "os"
	)


// GetRequest http request
func GetRequest(sURL string) []byte {
  sMethod := "GET"
	oClient := &http.Client{}

	req,  err := http.NewRequest(sMethod,sURL,nil)
    resp, err := oClient.Do(req)

	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
		// fmt.Printf("%s\n",resp.Status)
		defer resp.Body.Close()
		contents, _ := ioutil.ReadAll(resp.Body)
		return contents
	}

	return []byte("undef")
}

func main() {
	var sURL = "https://jsonplaceholder.typicode.com/todos/1"
	var byResponse = GetRequest(sURL)
	fmt.Println(string(byResponse))
}
