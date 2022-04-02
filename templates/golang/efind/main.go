package main

import (
	"bufio"
	"fmt"
	"flag"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

var sFilePath string
var sKeyword string
var sFileName string

func init() {
	flag.StringVar(&sFilePath, "path", "", "Folder path")
	flag.StringVar(&sKeyword,  "term", "", "Search terms")
	flag.StringVar(&sFileName, "name", "", "File Name")
	flag.Parse()
	if sFilePath == "" {
		flag.PrintDefaults()
		os.Exit(2)
	} 

	if sKeyword == "" && sFileName == "" {
			flag.PrintDefaults()
			os.Exit(2)
	}
}

func main() {

	if sKeyword != "" && sFileName != "" {
		fmt.Println("Cannot search for file name and string together.")
		os.Exit(2)
	} 

	fmt.Println("Getting files from " + sFilePath)
	fileList := GetFileList(sFilePath)

	if sKeyword != ""{
		DoSearch(fileList)
	} else {
		SearchFile(fileList)
	}

}

// GetFileList - get file list of folder
func GetFileList(sFilePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(py|cpp|pl|rb|js|html|h|go)$")

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

// Search file name recursively
func SearchFile(fileList []string){

	f, err := os.Create("serach_result.txt")

	if err != nil {
		panic(err)
	}

	defer f.Close()

	for _,file := range fileList {
		if strings.Contains(file,sFileName){
			sFile := file + "\n"
			f.WriteString(sFile)
			fmt.Print(sFile)
		}	
	}
}

// DoSearch - Search
func DoSearch(fileList []string){

	f, err := os.Create("serach_result.txt")

	if err != nil {
		panic(err)
	}

	defer f.Close()

	re , _:= regexp.Compile(sKeyword)

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

