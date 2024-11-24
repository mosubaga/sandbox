package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

const (
	url            = "[sURL]" // Replace with the target URL
	concurrentReqs = 10       // Number of concurrent requests
	totalBatches   = 10       // Number of batches
)

func sendRequest(wg *sync.WaitGroup, id int) {

	defer wg.Done()

	// Make the HTTP GET request
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Request %d failed: %v\n", id, err)
		return
	}
	defer resp.Body.Close()

	// Print response status for demonstration
	fmt.Printf("Request %d: %s\n", id, resp.Status)
}

func main() {

	for batch := 1; batch <= totalBatches; batch++ {
		fmt.Printf("Starting batch %d...\n", batch)

		var wg sync.WaitGroup

		for i := 1; i <= concurrentReqs; i++ {
			wg.Add(1)
			go sendRequest(&wg, (batch-1)*concurrentReqs+i)
		}

		// Wait for all goroutines in this batch to complete
		wg.Wait()
		fmt.Printf("Batch %d completed.\n", batch)

		// Optional delay between batches
		time.Sleep(1 * time.Second)
	}

	fmt.Println("All requests completed.")
}
