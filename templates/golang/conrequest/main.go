package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
	"strconv"
)

var sURL string
var sCount string

func init() {
	flag.StringVar(&sURL, "url", "", "URL to curl")
	flag.StringVar(&sCount, "count", "", "Number of concurrent requests to send")
	flag.Parse()
	if sURL == "" || sCount == "" {
		flag.PrintDefaults()
		os.Exit(2)
	}
}

func MakeRequest(url string, ch chan<-string) {
	start := time.Now()
	resp, _ := http.Get(url)
	secs := time.Since(start).Seconds()
	body, _ := ioutil.ReadAll(resp.Body)
	ch <- fmt.Sprintf("%.2f elapsed with response length: %d %s", secs, len(body), url)
}

func main() {
	start := time.Now()
	ch := make(chan string)

	icount,_ := strconv.Atoi(sCount)

	for i := 0; i < icount; i++ {
		go MakeRequest(sURL, ch)
	}

	for j := 0; j < icount; j++ {
	  fmt.Println(<-ch)
	}

	fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())