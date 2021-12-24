package main

import (
	"fmt"
	"github.com/gen2brain/go-unarr"
	"os"
	"path/filepath"
	"regexp"
)

func main() {

	sFilePath := "<ROOTFOLDER>"
	fmt.Println("Getting files from " + sFilePath)
	fileList := GetFileList(sFilePath)
	for _, file := range fileList {
		done := make(chan string)
		go ExtractArchive(done, sFilePath, file)
		msg := <-done
		fmt.Println("Completed: " + msg)
	}
}

// GetFileList - get file list of folder
func GetFileList(sFilePath string) []string {

	var fileList []string
	re, _ := regexp.Compile("^.*\\.(7z|zip|rar)$")

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

func ExtractArchive(done chan string, sDst string, sArchive string) {

	fmt.Printf("Extracting: " + sArchive + "\n")

	a, err := unarr.NewArchive(sArchive)
	if err != nil {
		panic(err)
	}
	defer a.Close()

	_, err = a.Extract(sDst)
	if err != nil {
		panic(err)
	}

	done <- string(sArchive)
}
