import pymongo

def querydb():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[{dbname}]
    mycol = mydb[{collection_name}]

    myquery = {[filter]}
    mydoc = mycol.find(myquery)

    for x in mydoc:
        sFirstName = x[{something}]
        print(f'{sFirstName}')

if __name__ == '__main__':
    querydb()

