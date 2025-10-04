package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func QueryTable(tableName string) ([]map[string]interface{}, error) {

	db, err := sql.Open("mysql", "[username]:[password]!@tcp([dbhost])/[dbname]")

	if err != nil {
		panic(err)
	}
	defer db.Close()
	fmt.Println("Connected to database")

	query := fmt.Sprintf("select * from %s", tableName)
	rows, err := db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	fmt.Println("Query executed successfully")

	// Get column names
	columns, err := rows.Columns()
	if err != nil {
		return nil, err
	}

	// Prepare result slice
	var results []map[string]interface{}

	// Iterate through rows
	for rows.Next() {
		// Create a slice of interface{} to hold each column value
		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))

		for i := range columns {
			valuePtrs[i] = &values[i]
		}

		// Scan the row into the value pointers
		if err := rows.Scan(valuePtrs...); err != nil {
			return nil, err
		}

		// Create a map for this row
		rowMap := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]

			// Convert byte arrays to strings
			if b, ok := val.([]byte); ok {
				v = string(b)
			} else {
				v = val
			}
			rowMap[col] = v
		}

		results = append(results, rowMap)
	}

	return results, nil
}

func main() {
	results, _ := QueryTable("[table_name]")
	for _, result := range results {
		fmt.Println(result["id"], result["name"])
	}
}
