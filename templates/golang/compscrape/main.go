package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"log"
	"net/http"
	"os"
	// "strings"
	"strconv"
)

func main() {

	f, err := os.Create("[CSV_NAME]")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	sHead := "SOMEHEADING\n"
	f.WriteString(sHead)
	if err != nil {
		return
	}

	for i := 1998; i < 2013; i++ {
		sYear := strconv.Itoa(i)
		sPlayers := GetPlayers(sYear)
		f.WriteString(sPlayers)
	}

	fmt.Println("-- Done--\n")
}

func GetPlayers(sYear string) string {

	// Make HTTP request
	sURL := "[SOMEURL]" + sYear + ".html"
	fmt.Println("[MSG] : " + sURL + "\n")
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

	sSelector := "[SELECTOR]"

	var sText string
	// Find and print image URLs
	document.Find(sSelector).Each(func(index int, element *goquery.Selection) {

		sText = ""
		element.Find("tr").Each(func(index int, child *goquery.Selection) {
			i := 0
			child.Find("td").Each(func(index int, gchild *goquery.Selection) {
				if i == 0 {
					sText += sYear + ","
				} else if i == 12 {
					sText += gchild.Text() + "\n"
				} else {
					sText += gchild.Text() + ","
				}
				i += 1
			})
		})
	})

	return sText
}
