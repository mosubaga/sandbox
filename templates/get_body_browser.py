# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re, json, pprint

class BrowserTest(unittest.TestCase):

    def CaptureError(self,logentries):

        iErrorCount = 0

        for jobj in logentries:
            if self.errorString in jobj['message']:
                iErrorCount+=1

        return iErrorCount

    def ExtractContent(self,browser,sURL):

        if browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "ie11":
            driver = webdriver.Ie()
        elif browser == "firefox":
            driver = webdriver.Firefox()
        elif browser == "safari":
            driver = webdriver.Safari()
        elif browser == "edge":
            driver = webdriver.Edge()
        else:
            quit("Error: Cannot define browser. Stopping test")

        driver.get(sURL)

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            sText = element.text
        except:
            print("Exception Error Occured")
        finally:
            driver.close()

        return sText

    def setUp(self):

        self.base_url    = "http://www.google.com"
        self.target_url  = "http://www.google.co.jp"

    def test_browser_chrome(self):

        browser = "chrome"
        sSrcText = self.ExtractContent(browser,self.base_url)
        sTgtText = self.ExtractContent(browser,self.target_url)

        assert sSrcText != sTgtText

    def test_browser_ie11(self):

        browser = "ie11"
        sSrcText = self.ExtractContent(browser,self.base_url)
        sTgtText = self.ExtractContent(browser,self.target_url)

        assert sSrcText != sTgtText

    def tearDown(self):
            print("Test Done")

if __name__ == "__main__":
    unittest.main()
