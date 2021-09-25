package main

import (
	"fmt"
	"net/http"
)

func getPage(url string) (int, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, err
	}

	defer resp.Body.Close()
	body := resp.StatusCode
	if err != nil {
		return 0, err
	}

	return body, nil
}

func worker(urlCh chan string, sizeCh chan string, id int) {
	for {
		url := <-urlCh
		length, err := getPage(url)
		if err == nil {
			sizeCh <- fmt.Sprintf("%s has length of %d :(%d)", url, length, id)
		} else {
			sizeCh <- fmt.Sprintf("Error getting %s : %s", url, err)
		}
	}
}

func generator(url string, urlCh chan string) {
	urlCh <- url
}

func main() {

	urls := []string{"https://www.google.com", "https://www.yahoo.com", "https://www.boston.com"}

	urlCh := make(chan string)
	sizeCh := make(chan string)

	for i := 0; i < 10; i++ {
		go worker(urlCh, sizeCh, i)
	}

	for _, url := range urls {
		go generator(url, urlCh)
	}

	for i := 0; i < len(urls); i++ {
		fmt.Printf("%s\n", <-sizeCh)
	}
}
