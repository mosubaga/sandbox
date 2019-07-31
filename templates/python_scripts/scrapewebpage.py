import sys
import shutil
import os
import re
import codecs
import urllib3
import pprint
import requests
import html5lib
from bs4 import BeautifulSoup

g_url="<URL>"

# ----------------------------------------------------
def get_url_content():
# ----------------------------------------------------

    response = requests.get(g_url)

    print(response.headers)

    soup = BeautifulSoup(response.content,'html5lib')
    links = soup.find_all('img',border=True)

    for link in links:
        print(link)

        #if link['alt'].exists:
        #    print(link['alt'])
        #if (len(link.text) > 0):
        #    print("[" + link['src'] + "]: " + link.text)


def main():
    get_url_content()


if __name__ == '__main__':
    main()
