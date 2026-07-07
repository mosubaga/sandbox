import psycopg

def connect_db():

    conn = psycopg.connect(
        host="localhost",
        port="[PORT]",
        user="[USERNAME]",
        password="[PASSWORD]",
        dbname="[DBNAME]"
    )

    cursor = conn.cursor()
    cursor.execute("[SQL QUERY]")

    for x in cursor.fetchall():
        print(x)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    connect_db()
