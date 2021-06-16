package main

import (
	"fmt"
	"strings"
	"github.com/PuerkitoBio/goquery"
	"log"
	"net/http"
)

func main() {
	// Make HTTP request
	sURL := "[URL]"
	response, err := http.Get(sURL)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()

	// Create a goquery document from the HTTP response
	document, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal("Error loading HTTP response body. ", err)
	}

	// Find and print image URLs
	document.Find("tr").Each(func(index int, element *goquery.Selection) {

		sText := ""
		element.Find("td").Each(func(index int, child *goquery.Selection){

			if (index < 5){
				sText += child.Text() + ","
			}
			if (index == 5) {
				sText += child.Text()
			}
		})

		fmt.Println(strings.TrimSpace(sText))
	})
}
