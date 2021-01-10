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

var keyword = "[keyword]"

func main() {
	iArgLength := len(os.Args)
	sFilePath := CheckArgument(iArgLength)
	fmt.Println("Getting files from " + sFilePath)
	fileList := GetFileList(sFilePath)
	DoSearch(fileList)
}

func CheckArgument(iLenArg int) string {
	sFilePath := "[FilePath]"
	fmt.Println(iLenArg)

	if len(os.Args) > 1 {
		return os.Args[1]
	} else {
		return sFilePath
	}
}

// GetFileList - get file list of folder
func GetFileList(sFilePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(py|cpp|pl|rb|js)$")

	err := filepath.Walk(sFilePath, func(path string, f os.FileInfo, err error) error {
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

// DoSearch - Search
func DoSearch(fileList []string){

	f, err := os.Create("[FilePath]/serach_result.txt")

	if err != nil {
		panic(err)
	}

	re , _:= regexp.Compile(keyword)

	for _,file := range fileList {
		lines := File2lines(file)
		for j, line := range lines{
			if re.MatchString(line){
				line := strings.TrimSpace(line)
				oh := "[" + file + "] (" +strconv.Itoa(j+1) +"): " + line + "\n"
				f.WriteString(oh)
				fmt.Print(oh)
			}
		}
	}
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
