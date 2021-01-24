import sys, shutil, os, re, codecs
import urllib3, requests, html5lib
import pprint
from bs4 import BeautifulSoup

g_url      = "[URL]"
g_selector = "[selector]"
sPlayer    = "[Name]"

# ----------------------------------------------------
def get_url_content():
# ----------------------------------------------------

    print("Getting info...")
    response = requests.get(g_url)

    print(response.status_code)

    soup = BeautifulSoup(response.content,'html5lib')
    iTable = soup.select(g_selector)
    iRows = iTable[0].find_all("tr")
    
    i=0
    print("NAME,YEAR,G,HR,RBI,SB,AVG")
    for r in iRows:
        num = r.find_all("td")
        if (len(num) > 0):
            i+=1
            if (i == 1):
                print(f'{sPlayer},{num[0].text.strip()},{num[2].text.strip()},{num[9].text.strip()},{num[11].text.strip()},{num[12].text.strip()},{num[21].text.strip()}')
            else:
                print(f'{sPlayer},{num[0].text.strip()},{num[1].text.strip()},{num[8].text.strip()},{num[10].text.strip()},{num[11].text.strip()},{num[20].text.strip()}')


def main():
    get_url_content()

if __name__ == '__main__':
    main()