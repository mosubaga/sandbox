#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys, shutil, os, re, codecs, pprint
import requests, json, urllib3

# ----------------------------------------
def getJSON():
# ----------------------------------------
    with codecs.open("data.json", "r", encoding='utf-8') as dataFile:
        data = dataFile.read()
    return data


# ----------------------------------------
def prettifyJSON(sBody):
# ----------------------------------------

    oJSON = json.loads(sBody)
    sFormatJSON = json.dumps(oJSON, ensure_ascii = False, indent=4)
    return sFormatJSON


# ----------------------------------------
def RunTestGET(sURL):
# ----------------------------------------
    headers = {'content-type': 'application/json'}
    resp   = requests.get(sURL, headers=headers, verify=False)
    body   = prettifyJSON(resp.content)
    resp.connection.close()
    print(prettifyJSON(body))



# ----------------------------------------
def RunTestPOST(sURL):
# ----------------------------------------
    sData  = getJSON()
    headers = {'content-type': 'application/json'}
    resp   = requests.post(sURL, data=sData, headers=headers, verify=False)
    body   = prettifyJSON(resp.content)
    resp.connection.close()
    print(resp.status_code)
    print(body)


# ----------------------------------------
def RunTestPUT(sURL):
# ----------------------------------------
    sData  = getJSON()
    headers = {'content-type': 'application/json'}
    resp   = requests.put(sURL, data=sData, headers=headers, verify=False)
    body   = prettifyJSON(resp.content)
    resp.connection.close()
    print(resp.status_code)
    print(body)


# ----------------------------------------
def RunTestPATCH(sURL):
# ----------------------------------------
    sData  = getJSON()
    headers = {'content-type': 'application/json'}
    resp   = requests.patch(sURL, data=sData, headers=headers, verify=False)
    body   = prettifyJSON(resp.content)
    resp.connection.close()
    print(resp.status_code)
    print(body)


# ----------------------------------------
def RunTestDELETE(sURL):
# ----------------------------------------
    headers = {'content-type': 'application/json'}
    resp   = requests.delete(sURL, headers=headers, verify=False)
    body   = prettifyJSON(resp.content)
    resp.connection.close()
    print(resp.status_code)
    print(body)

# ----------------------------------------
def main():
# ----------------------------------------

    sMethod = sys.argv[1]
    sURI    = sys.argv[2]

    urllib3.disable_warnings()
    sURL = "[URL]" + sURI
    if (re.search("get|GET",sMethod)):
        print("GET Method")
        RunTestGET(sURL)
    elif (re.search("post|POST",sMethod)):
        print("POST Method")
        RunTestPOST(sURL)
    elif (re.search("put|PUT",sMethod)):
        print("PUT Method")
        RunTestPUT(sURL)
    elif (re.search("patch|PATCH",sMethod)):
        print("PATCH Method")
        RunTestPATCH(sURL)
    elif (re.search("delete|DELETE",sMethod)):
        print("DELETE Method")
        RunTestDELETE(sURL)
    else:
        print(":: ERROR :: UNKNOWN METHOD")

if __name__ == '__main__':
    main()
