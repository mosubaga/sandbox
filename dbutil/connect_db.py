import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port="[PORT]",
  user="[USERNAME]",
  passwd="[PASSWD]",
  database="[DBNAME]"
)

# print(mydb) 

cursor = mydb.cursor()
query = "[SQL STATEMENT]"

cursor.execute(query)
myresult = cursor.fetchall()

for x in myresult:
  print(f"Name: {x[0]} HR: {x[12]}")

mydb.close()
