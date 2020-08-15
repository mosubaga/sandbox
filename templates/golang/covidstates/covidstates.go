package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type Figure struct {
	Cases int `json:"positiveIncrease"`
	Deaths int `json:"deathIncrease"`
	Hospitalized int `json:"hospitalizedIncrease"`
}


func main() {

	sURL:="https://api.covidtracking.com/v1/states/ma/daily.json"

	response, err := http.Get(sURL)
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
		defer response.Body.Close()
		contents, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Printf("%s", err)
			os.Exit(1)
		}

		var datas []Figure
		msg:=json.Unmarshal([]byte(contents),&datas)
		if msg != nil{
			fmt.Println("Error::",msg)
		}

		for i := len(datas)-1; i >= 0; i--  {
		fmt.Printf("%v\n",datas[i].Deaths)
		}
	}
}
