package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"
)

type JCharacter struct {
	Id         int    `json:"id"`
	Cname      string `json:"cname"`
	Cclass     string `json:"cclass"`
	Clevel     int    `json:"clevel"`
	Cphysical  string `json:"cphysical"`
	Cfire      string `json:"cfire"`
	Cice       string `json:"cice"`
	Clightning string `json:"clightning"`
	Cwind      string `json:"cwind"`
	Clight     string `json:"clight"`
	Cdark      string `json:"cdark"`
}

type JChars []JCharacter

func gencsv() {

	// open file
	f, err := os.Open("[CSV]")
	if err != nil {
		log.Fatal(err)
	}

	r := csv.NewReader(f)
	records, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	for _, line := range records {

		fmt.Println(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10])
	}
}

func megatencsv() {

	// open file
	f, err := os.Open("[CSVFILE]")
	if err != nil {
		log.Fatal(err)
	}

	r := csv.NewReader(f)
	records, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	var megatenchars JChars

	for _, line := range records {
		iid, _ := strconv.Atoi(line[0])
		ilevel, _ := strconv.Atoi(line[3])
		var character = JCharacter{Id: iid, Cname: line[1], Cclass: line[2], Clevel: ilevel, Cphysical: line[4], Cfire: line[5], Cice: line[6], Clightning: line[7], Cwind: line[8], Clight: line[9], Cdark: line[10]}
		megatenchars = append(megatenchars, character)
	}

	j, _ := json.MarshalIndent(megatenchars, "", "  ")
	sjson := string(j)

	fj, err := os.Create("[JSONFILE]")

	if err != nil {
		log.Fatal(err)
	}

	fw, err := fj.WriteString(sjson)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("json: %v\n", fw)

}

func main() {
	megatencsv()
}
