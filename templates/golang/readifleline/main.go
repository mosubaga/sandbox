package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// Readlines :: An iterator that returns one line of a file at a time.
func Readlines(path string) (<-chan string, error) {
	fobj, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	scanner := bufio.NewScanner(fobj)
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	chnl := make(chan string)
	go func() {
		for scanner.Scan() {
			chnl <- scanner.Text()
		}
		close(chnl)
	}()

	return chnl, nil
}

func SyncReadLines(filePath string) ([]string, error) {
	f, err := os.Open(filePath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, err)
	}

	return lines, nil
}

func main() {
	sFile := "[TEXT_FILE]"
	reader, err := Readlines(sFile)
	if err != nil {
		log.Fatal(err)
	}

	for line := range reader {
		if strings.Contains(line, "[KEYWORD]") {
			fmt.Println(line)
		}
	}

}
