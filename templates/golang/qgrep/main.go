package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

var sPath string
var sKeyword string

func init() {
	flag.StringVar(&sPath, "path", "[FilePath]", "Path to search")
	flag.StringVar(&sKeyword, "keyword", "[KeyWord]", "Keyword to search")
	flag.Parse()
	if sPath == "" {
		flag.PrintDefaults()
		os.Exit(2)
	}
}

func main() {

	fileList := GetFileList(sPath)
	DoSearch(fileList, sKeyword)
}

// GetFileList - get file list of folder
func GetFileList(filePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(py|pl|cpp|h|hpp|js|ts|rb|rs|go|html|css)$")

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

func DoSearch(fileList []string, sKeyword string) {

	for _, file := range fileList {
		lines := File2lines(file)
		for j, line := range lines {
			if strings.Contains(line, sKeyword) {
				line := strings.TrimSpace(line)
				oh := "[" + file + "] (" + strconv.Itoa(j+1) + "): " + line + "\n"
				fmt.Print(oh)
			}
		}
	}
}

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
