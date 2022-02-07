import csv
import json
import codecs

def csv_to_json(sName):
    jsonArray = []

    csvFilePath  = sName + ".csv"
    jsonFilePath = sName + ".json"

    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:

        csvReader = csv.DictReader(csvf)

        #convert each csv row into python dict
        for row in csvReader:
            #add this python dict to json array
            jsonArray.append(row)

    #convert python jsonArray to JSON String and write to file
    with codecs.open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

def main():
    csv_to_json("[NAME]")

if __name__== "__main__" :
     main()
