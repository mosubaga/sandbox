package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
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

func grep(line string, key string) bool {
	if strings.Contains(line, key) {
		return true
	}
	return false
}

func CleanString(line string) string {

	r := "\"(?P<key>.*)\": \"(?P<value>.*)\""
	re := regexp.MustCompile(r)

	re = regexp.MustCompile(r)

	m := map[string]string{}
	names := re.SubexpNames()
	for i, n := range re.FindStringSubmatch(line) {
		m[names[i]] = n
	}

	sOutput := m["value"]

	return sOutput
}

// Parse JSON file
func ParseJSON(sPath string) {

	contents, err := ioutil.ReadFile(sPath)
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
		// Declared an empty interface of type Array
		var results []map[string]interface{}

		// Unmarshal or Decode the JSON to the interface.
		json.Unmarshal([]byte(contents), &results)

		for _, result := range results {
			//Reading each value by its key
			sName := fmt.Sprintf("%v", result["NAME"])
			sStr := fmt.Sprintf("%v", result["STR"])
			fmt.Println(strings.TrimSpace(sName), strings.TrimSpace(sStr))
		}
	}

}

func main() {
	reader, err := Readlines("<json>.json")
	if err != nil {
		log.Fatal(err)
	}

	for line := range reader {
		if grep(line, "NAME") {
			fmt.Println(CleanString(line))
		}
	}

	ParseJSON("<json>.json")
}
