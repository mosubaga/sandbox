package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type RImg struct {
	IID int `json:"iid"`
	SName string `json:"sname"`
	SImg string `json:"simage"`
}

type RImgs []RImg

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

func handler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Access-Control-Allow-Origin", "*")
	fmt.Fprintf(writer, "API is working")
}


func imghandler(writer http.ResponseWriter, request *http.Request){

	writer.Header().Set("Access-Control-Allow-Origin", "*")
	writer.Header().Set("Content-Type", "application/json")
	sCsvFile := "[csvfile]"

	// Open the file
	csvfile, err := os.Open(sCsvFile)
	if err != nil {
		log.Fatalln("Couldn't open the csv file", err)
	}
	defer csvfile.Close()

	r := csv.NewReader(csvfile)
	var aSan RImgs
	var sImg string
	var sName string
	i := 0

	for {

		i++
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		sName = record[0]
		sImg = record[1]

		oSan:=RImg{i,sName,sImg}
		aSan = append(aSan,oSan)
	}

	json.NewEncoder(writer).Encode(aSan)
}

func main() {
	http.HandleFunc("/", handler)
	http.HandleFunc("/api/img", imghandler)
	fmt.Println("Listening to port 3000")
	http.ListenAndServe(":3000", nil)
}


