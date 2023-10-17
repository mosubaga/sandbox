# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import codecs, re, os, pprint
import lxml.html
import requests

#trick to parse UTF-8 for pyquery
UTF8_PARSER = lxml.html.HTMLParser(encoding='utf-8')

def getdata(sURL, sCSV):

    r = requests.get(sURL)
    doc = pq(lxml.html.fromstring(r.content, parser=UTF8_PARSER))

    selector = "[SELECTOR]"

    with open(sCSV, "w", encoding="utf-8") as fout:
        entries = doc(selector)
        for entry in entries:
            attribs = entry.getchildren()
            wname = attribs[0].text
            if (wname == None):
                links = attribs[0].getchildren()
                wname = links[0].text

            wt = attribs[3].text
            wtype = attribs[4].text
            watk = attribs[5].text
            wroute = attribs[8].text
            if (wtype != None):
                fout.write("{},{},{},{},{}\n".format(wname,wt,wtype,watk,wroute))

def main():

    getdata("[sURL]","[sCSV]")

if __name__ == '__main__':
    main()

