package main

import (
    "fmt"
    "github.com/tebeka/selenium"
    "github.com/tebeka/selenium/chrome"
)

func main() {
    // Run Chrome browser
    service, err := selenium.NewChromeDriverService("./chromedriver.exe", 4444)
    if err != nil {
        panic(err)
    }
    defer service.Stop()

    caps := selenium.Capabilities{}
    caps.AddChrome(chrome.Capabilities{Args: []string{
        "window-size=1920x1080",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "disable-gpu",
        // "--headless",  // comment out this line to see the browser
    }})

    driver, err := selenium.NewRemote(caps, "")
    defer driver.Close()
    if err != nil {
        panic(err)
    }

    cssselector := "body"

    sURL := "[URL]"

    driver.WaitWithTimeoutAndInterval(waitcomplete, 1000, 1000)
    driver.Get(sURL)

    el, gerr := driver.FindElement("css selector", cssselector)

    if gerr != nil {
        panic(gerr)
    }

    stext , _ := el.Text()
    fmt.Printf("%s", stext)
}

func waitcomplete(driver selenium.WebDriver) (bool, error) {

    cssselector := "body"
    we, _ := driver.FindElement("css selector", cssselector)

    return we.IsDisplayed()
}
