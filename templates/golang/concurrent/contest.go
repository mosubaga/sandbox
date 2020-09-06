package main

import (
    "fmt"
	"net/http"
    "os"
	)

// GetRequest http request
func GetRequest(done chan string, sURL string) {
    sMethod := "GET"
	oClient := &http.Client{} 
	
	req,  err := http.NewRequest(sMethod,sURL,nil)
    resp, err := oClient.Do(req)
    fmt.Println(sURL)
	
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
        // fmt.Printf("%s\n",resp.Status)
		defer resp.Body.Close()
		// contents, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			fmt.Printf("%s", err)
			os.Exit(1)
		} 
        done <- string(resp.Status)
	}
}

func main() {

    var aURL [2]string 
    aURL[0] = "https://www.google.com?q=golang" 
    aURL[1] = "https://www.google.com?q=ruby"

    // done := make(chan string)
    for i := 0; i < len(aURL); i++ {
        done := make(chan string)
        go GetRequest(done, aURL[i])
        msg := <- done
        fmt.Println("Response:" + msg)
    }

    fmt.Println(":: Done Testing ::")
}
