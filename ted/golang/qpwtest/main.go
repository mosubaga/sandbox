package main

import (
	"fmt"
	"log"
	"time"

	"github.com/playwright-community/playwright-go"
)

func main() {

	// err := playwright.Install()

	// Start Playwright
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("could not start Playwright: %v", err)
	}
	defer pw.Stop()

	// Launch the browser
	browser, err := pw.Chromium.Launch()
	if err != nil {
		log.Fatalf("could not launch browser: %v", err)
	}
	defer browser.Close()

	// Create a new browser context
	context, err := browser.NewContext()
	if err != nil {
		log.Fatalf("could not create browser context: %v", err)
	}
	defer context.Close()

	// Set a cookie

	sDomain := "[Domain]"
	sPath := "/"

	err = context.AddCookies([]playwright.OptionalCookie{
		{
			Name:   "[name]",
			Value:  "[value]",
			Domain: playwright.String(sDomain),
			Path:   playwright.String(sPath),
		},
	})
	if err != nil {
		log.Fatalf("could not set cookies: %v", err)
	}

	time.Sleep(1 * time.Second)

	// Create a new page in the context
	page, err := context.NewPage()
	if err != nil {
		log.Fatalf("could not create page: %v", err)
	}

	// Navigate to the website
	if _, err := page.Goto("[sURL]"); err != nil {
		log.Fatalf("could not navigate to example.com: %v", err)
	}

	time.Sleep(2 * time.Second)

	// #comp-l3w07syq0 > a
	entries, err := page.Locator("a[data-testid=\"linkElement\"]").All()
	for i, entry := range entries {
		title, err := entry.InnerText()
		if err != nil {
			log.Fatalf("could not get text content: %v", err)
		}

		if len(title) > 1 {
			fmt.Printf("%d: %s\n", i+1, title)
		}
	}

}
