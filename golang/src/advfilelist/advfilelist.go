package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

var keyword = "[KEYWORD]"

func main() {
	filePath := "[FILEPATH]"
	fileList := GetFileList(filePath)
	DoSearch(fileList)
}

// DoSearch - Search
func DoSearch(fileList []string) {

	f, err := os.Create("[TEXTFILE]")

	if err != nil {
		panic(err)
	}

	re, _ := regexp.Compile(keyword)

	for _, file := range fileList {
		lines := File2lines(file)
		for j, line := range lines {
			if re.MatchString(line) {
				line := strings.TrimSpace(line)
				oh := "[" + file + "] (" + strconv.Itoa(j+1) + "): " + line + "\n"
				f.WriteString(oh)
			}
		}
	}
}

// GetFileList - Get file list
func GetFileList(filePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(html|js|css)$")

	err := filepath.Walk(filePath, func(path string, f os.FileInfo, err error) error {
		if re.MatchString(path) {
			fileList = append(fileList, path)
		}
		return nil
	})

	if err != nil {
		panic(err)
	}

	return fileList
}

// File2lines - Write to file
func File2lines(filePath string) []string {
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

	return lines
}
