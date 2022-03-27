package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

var sURL string
var sOutFile string

func init() {
	flag.StringVar(&sURL, "url", "", "URL to curl")
	flag.StringVar(&sOutFile, "output", "output.json", "Output file")
	flag.Parse()
	if sURL == "" || sOutFile == "" {
		flag.PrintDefaults()
		os.Exit(2)
	}
}

func PrettyString(str *string) string {
	var prettyJSON bytes.Buffer

	// Return the input string if input has errors
	if err := json.Indent(&prettyJSON, []byte(*str), "", "    "); err != nil {
		fmt.Println("WARNING: Not in JSON form despite header says it. Please see error below. Returning the raw content anyways... ")
		fmt.Println(err)
		return *str
	}
	return prettyJSON.String()
}

func mCurlGet(sURL string, sfilePath string) {

	req, err := http.NewRequest("GET", sURL, nil)
	req.Header.Add("Authorization", "[AuthUser]")
	response, err := http.DefaultClient.Do(req)

	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	} else {
		defer response.Body.Close()
		responsetype := response.Header.Get("Content-Type")
		fmt.Printf("Status Code: %d\n", response.StatusCode)
		contents, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Printf("%s", err)
			os.Exit(1)
		} else {
			f, err := os.Create(sfilePath)
			if err != nil {
				panic(err)
			}
			defer f.Close()

			sOutput := string(contents)

			if responsetype == "application/json" {
				sOutput = PrettyString(&sOutput)
			}

			f.WriteString(sOutput)
		}
	}
}

func main() {
	mCurlGet(sURL, sOutFile)
}
