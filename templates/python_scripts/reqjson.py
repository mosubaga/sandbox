import sys, shutil, os, re, codecs, pprint
import requests, json

def GetJSON(sURL):
    jText = requests.get(sURL).text
    parseJSON = json.loads(jText)
    sSourceTextList = parseJSON['[key1]']
    ListCount = len(sSourceTextList)
    print(ListCount)

    for x in range(1,ListCount-3):
        print(sSourceTextList[x]['[key2]'])

# ----------------------------------------------
def main():
# ----------------------------------------------
    sURL ='[URL]'
    GetJSON(sURL)

if __name__ == '__main__':
    main()
