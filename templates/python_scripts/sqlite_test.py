import sqlite3

def main():
    conn = sqlite3.connect(r'[DBPATH]')
    print("Opened database successfully")

    cursor = conn.execute("select * from region")

    for row in cursor:
       print(str(row[0]) + "=" +row[1])

    conn.close()
    print("Closed database successfully")

if __name__ == '__main__':
    main()
