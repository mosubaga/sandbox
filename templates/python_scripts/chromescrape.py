from requestium import Session


def set_cookie_and_scrape(url, cookie_name, cookie_value):
    # Create a session
    s = Session(webdriver_path='./chromedriver',
                browser='chrome',
                default_timeout=15,
                webdriver_options={
                    'arguments': ['headless']
                })

    # Set the cookie
    s.driver.get(url)
    s.driver.add_cookie({'name': cookie_name, 'value': cookie_value})

    # Reload the page to apply the cookie
    s.driver.get(url)

    # Wait for the page to load completely
    s.driver.implicitly_wait(10)

    # Scrape text from the website
    cssselector = '[css]'
    text = s.driver.ensure_element_by_css_selector(cssselector).get_attribute('textContent')

    # Close the session
    s.driver.quit()

    return text


if __name__ == '__main__':
    url = '[url]'
    cookie_name = '[name]'
    cookie_value = '[value]'

    scraped_text = set_cookie_and_scrape(url, cookie_name, cookie_value)
    print(scraped_text)

