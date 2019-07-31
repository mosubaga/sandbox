package main

import (
"fmt"
"net/http"
"io/ioutil"
"encoding/json"
"strconv"
"os"
)

type Book struct {
  ID int `json:"id"`
  Title string `json:"title"`
}

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

  // Taken from JSONPlaceholder : https://jsonplaceholder.typicode.com/
	var sURL = "https://jsonplaceholder.typicode.com/todos"
	var sResponse = string(GetRequest(sURL))

  var stext []Book
  json.Unmarshal([]byte(sResponse), &stext)

  for i := 0; i < len(stext); i++ {
    var sID = strconv.Itoa(stext[i].ID)
    fmt.Println(sID + ": " + stext[i].Title)
	}
}
