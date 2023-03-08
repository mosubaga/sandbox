package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
)

func main() {

    sURL := "[URL]"

    client := &http.Client{}
    req, err := http.NewRequest("GET", sURL, nil)
    req.Header.Add("Authorization","<HEADER>")
    response, err := client.Do(req)

    if err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    } else {
        defer response.Body.Close()
        contents, err := ioutil.ReadAll(response.Body)
        if err != nil {
            fmt.Printf("%s", err)
            os.Exit(1)
        } else {
            // Declared an empty interface of type Array
            var results map[string]interface{}

            // Unmarshal or Decode the JSON to the interface.
            json.Unmarshal([]byte(contents), &results)

            segments := results["segments"].([]interface{})

            for _, segment := range segments {
                text  := segment.(map[string]interface{})

                if tgt, ok := text["target_text"]; ok {
                    fmt.Printf("Source: %v\n",text["[field]"])
                    fmt.Printf("Target: %v\n\n",tgt)
                }
            }
        }
    }
}

