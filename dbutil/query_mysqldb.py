import mysql.connector

def connect_db():

    mydb = mysql.connector.connect(
        host="localhost",
        user="[username]",
        password="[password]",
        database="[dbname]"
    )

    mycursor = mydb.cursor()
    mycursor.execute("[SQL QUERY]")

    for x in mycursor:
    	print(x)

if __name__ == '__main__':
    connect_db()

