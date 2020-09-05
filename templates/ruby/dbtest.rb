require "mysql"

begin

  dbh = Mysql.new 'localhost','[user]','[password]','[dbname]' 
  sql_statement = '[SQL STATMENT]'
  rs = dbh.query(sql_statement)
  n_rows = rs.num_rows

  puts "There are #{n_rows} rows in the result set:\n\n"

  n_rows.times do
    puts rs.fetch_row.join("\s")
  end
rescue Mysql::Error => e
  puts "Error code: #{e.errno}"
  puts "Error message: #{e.error}"
  puts "Error SQLSTATE: #{e.sqlstate}" if e.respond_to?("sqlstate")
ensure
  # disconnect from server
  dbh.close if dbh
end
