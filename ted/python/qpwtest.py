from playwright.sync_api import sync_playwright

def get_page_title_with_cookie(url):

    with sync_playwright() as p:
        
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        context.add_cookies([{
            "name": "[name]",
            "value": "[value]",
            "domain": url.split("//")[1].split("/")[0],  # Extract domain from URL
            "path": "/",
            "httpOnly": False,
            "secure": False
        }])

        # Create a new page
        page = context.new_page()

        # Navigate to the target URL
        page.goto(url,wait_until="networkidle")

        # Get the page title
        title = page.title()

        # Close the browser
        browser.close()

        return title

def main():

    # Specify the URL
    target_url = "[sURL]"  # Replace with your target URL

    # Get and print the page title
    page_title = get_page_title_with_cookie(target_url)
    print(f"Page title: {page_title}")


if __name__ == "__main__":

    main()
