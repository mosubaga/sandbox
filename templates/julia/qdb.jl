using MySQL

dbconn = DBInterface.connect(MySQL.Connection, "[HOST]", "[USER]", "[PASSWD]", db = "[DBNAME]")

sql = "[SQL]"
rows = DBInterface.execute(dbconn, sql)

for row in rows
    println(row[:origin_name], " == ", row[:project_key])
end