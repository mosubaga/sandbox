package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
)

func main() {
	filePath := "<GETDIR>"
	fileList := GetFileList(filePath)

	for i, file := range fileList {
		fmt.Printf("File #%d: %s\n", i, file)
	}
}

// GetFileList - get file list of folder
func GetFileList(filePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(py)$")

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
