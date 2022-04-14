package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"time"

	"github.com/gen2brain/go-unarr"
)

var sFilePath string = "[FILE_PATH]"

func main() {

	fmt.Println("Getting files from " + sFilePath)
	fileList := GetFileList(sFilePath)

	ZipChannel := make(chan string, len(fileList))
	defer close(ZipChannel)
	for _, file := range fileList {
		go ExtractArchive(ZipChannel, file)
		<-ZipChannel
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

func ExtractArchive(ZipChannel chan<- string, sArchive string) {

	a, err := unarr.NewArchive(sArchive)
	if err != nil {
		panic(err)
	}
	defer a.Close()

	_, err = a.Extract(sFilePath)
	if err != nil {
		panic(err)
	}

	fmt.Printf(":: %s :: Unzipped %s\n", time.Now().Format("2006.01.02 15:04:05"), sArchive)
	ZipChannel <- string(sArchive)
}
