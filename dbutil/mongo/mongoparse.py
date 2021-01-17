import pymongo

def querydb():

    myclient = pymongo.MongoClient([mongodb])
    mydb = myclient[dbname]
    mycol = mydb[colnuame]

    myquery = {[filter_name]}
    mydoc = mycol.find(myquery)

    for x in mydoc:
        row = x[row]
        print(f'{row]')

if __name__ == '__main__':
    querydb()

