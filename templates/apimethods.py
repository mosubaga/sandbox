import sys, shutil, os, re, codecs, pprint
import requests

# ----------------------------------------
def getJSON():
# ----------------------------------------
    with codecs.open("data.json", "r", encoding='utf-8') as dataFile:
        data = dataFile.read()
    return data

# ----------------------------------------
def RunTestGET(sURL):
# ----------------------------------------
    print(sURL)
    resp   = requests.get(sURL)
    body   = resp.content.decode("utf-8")
    resp.connection.close()
    print(resp.status_code)
    print(body)
    

# ----------------------------------------
def RunTestPOST(sURL):
# ----------------------------------------  
    sData  = getJSON()
    resp   = requests.post(sURL, data=sData)
    body   = resp.content.decode("utf-8")
    resp.connection.close()
    print(resp.status_code)
    print(body)

# ----------------------------------------
def RunTestPUT(sURL):
# ----------------------------------------
    sData  = getJSON()
    resp   = requests.put(sURL, data=sData)
    body   = resp.content.decode("utf-8")
    resp.connection.close()
    print(resp.status_code)
    print(body)

# ----------------------------------------
def RunTestDELETE(sURL):
# ----------------------------------------
    resp   = requests.delete(sURL)
    body   = resp.content.decode("utf-8")
    resp.connection.close()
    print(resp.status_code)
    print(body)

# ----------------------------------------
def main():
# ----------------------------------------
    
    sMethod = sys.argv[1]
    sApp    = sys.argv[2]
    sURI    = sys.argv[3]

    AppName = {}
    # XAPIS LOCAL
    AppName['<prod>']  = "<prod_url>"

    sURL = AppName[sApp] + sURI
    if (re.search("get|GET",sMethod)):
        print("GET Method")
        RunTestGET(sURL)
    elif (re.search("post|POST",sMethod)):
        print("POST Method")
        RunTestPOST(sURL)
    elif (re.search("put|PUT",sMethod)):
        print("PUT Method")
        RunTestPUT(sURL)
    elif (re.search("delete|DELETE",sMethod)):
        print("DELETE Method")
        RunTestDELETE(sURL)
    else:
        print(":: ERROR :: UNKNOWN METHOD")

if __name__ == '__main__':
    main()
    

