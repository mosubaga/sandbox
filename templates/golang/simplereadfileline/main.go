package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	path := "[TEXT_FILE]"
	fobj, _ := os.Open(path)
	scanner := bufio.NewScanner(fobj)

	chnl := make(chan string)
	go func() {
		for scanner.Scan() {
			chnl <- scanner.Text()
		}
		close(chnl)
	}()

	for line := range chnl {
		fmt.Println(line)
	}
}
