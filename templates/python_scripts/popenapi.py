import sys, shutil, os, re, pprint, datetime
import json


def parseJSONTags(jsonFile):
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
        tagsList = data['tags']
        for tag in tagsList:
            print(tag['name'])
            print(tag['description'])
            print()

def parseJSONPaths(jsonFile):
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
        pathsList = data['paths']
        for path in pathsList:
                methods = pathsList[path].keys()
                for method in methods:
                    print("Description: %s,%s,%s" % (method.upper(), path, pathsList[path][method]['description']))
                    if ("summary" in pathsList[path][method]):
                        print("Summary: %s,%s,%s" % (method.upper(), path, pathsList[path][method]['summary']))

def main():
    parseJSONPaths("whatever.json")
        
if __name__ == '__main__':
    main()