package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"reflect"
	"os"
)

func main() {

	sURL := "https://api.covidtracking.com/v1/states/current.json"

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

		var ojson interface{}
		json.Unmarshal([]byte(contents), &ojson)
		fmt.Println(reflect.TypeOf(ojson))
		result := ojson.([]interface{})

		for k,v := range result {

			val := v.(map[string]interface{})
			fmt.Println(k, val["state"], val["positive"])

			/*
			switch vv := v.(type) {
			case bool:
				fmt.Println(k,"is boolean", vv)
			case string:
				fmt.Println(k, "is string", vv)
			case int:
				fmt.Println(k, "is int", vv)
			case []interface{}:
				// fmt.Println(k, "is an array:")
				/*for i,u := range vv {
					//fmt.Println(i,u)
					val := u.(map[string]interface{})
					fmt.Println(i,val["base_domain"])
				}
			default:
				fmt.Println(k, "actual type:" , reflect.TypeOf(k))
			}*/
		}
	}
}
