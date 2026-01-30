package main

import (
	"database/sql"
	"encoding/gob"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

func CreateConnection(inputPath string, outputPath string) error {
	jsonData, err := os.ReadFile(inputPath)
	if err != nil {
		return fmt.Errorf("error reading json file: %v", err)
	}

	var connectionMap map[string]string
	err = json.Unmarshal(jsonData, &connectionMap)
	if err != nil {
		return fmt.Errorf("error unmarshaling json: %v", err)
	}

	outputFile, err := os.Create(outputPath)
	if err != nil {
		return fmt.Errorf("error creating gob file: %v", err)
	}
	defer outputFile.Close()

	encoder := gob.NewEncoder(outputFile)
	err = encoder.Encode(connectionMap)
	if err != nil {
		return fmt.Errorf("error encoding gob: %v", err)
	}

	fmt.Printf("Connection map saved to %s\n", outputPath)
	return nil
}

func QueryDatabase(gobPath string, query string, queryFilePath string, asCSV bool) error {
	gobFile, err := os.Open(gobPath)
	if err != nil {
		return fmt.Errorf("error opening gob file: %v", err)
	}
	defer gobFile.Close()

	var connectionMap map[string]string
	decoder := gob.NewDecoder(gobFile)
	err = decoder.Decode(&connectionMap)
	if err != nil {
		return fmt.Errorf("error decoding gob: %v", err)
	}

	sqlQuery := query
	if queryFilePath != "" {
		content, err := os.ReadFile(queryFilePath)
		if err != nil {
			return fmt.Errorf("error reading sql file: %v", err)
		}
		sqlQuery = string(content)
	}

	if sqlQuery == "" {
		return fmt.Errorf("no SQL query provided")
	}

	// Construct DSN: username:password@tcp(host)/database
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s",
		connectionMap["username"],
		connectionMap["password"],
		connectionMap["host"],
		connectionMap["database"],
	)

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return fmt.Errorf("error connecting to database: %v", err)
	}
	defer db.Close()

	rows, err := db.Query(sqlQuery)
	if err != nil {
		return fmt.Errorf("error executing query: %v", err)
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		return fmt.Errorf("error getting columns: %v", err)
	}

	isSelect := strings.HasPrefix(strings.ToUpper(strings.TrimSpace(sqlQuery)), "SELECT")

	if asCSV && isSelect {
		for i, col := range columns {
			fmt.Print(col)
			if i < len(columns)-1 {
				fmt.Print(",")
			}
		}
		fmt.Println()
	}

	values := make([]sql.RawBytes, len(columns))
	scanArgs := make([]interface{}, len(values))
	for i := range values {
		scanArgs[i] = &values[i]
	}

	for rows.Next() {
		err = rows.Scan(scanArgs...)
		if err != nil {
			return fmt.Errorf("error scanning row: %v", err)
		}

		if asCSV && isSelect {
			for i, col := range values {
				if col == nil {
					fmt.Print("NULL")
				} else {
					fmt.Print(string(col))
				}
				if i < len(values)-1 {
					fmt.Print(",")
				}
			}
			fmt.Println()
		} else {
			for i, col := range values {
				var value string
				if col == nil {
					value = "NULL"
				} else {
					value = string(col)
				}
				fmt.Printf("%s: %s ", columns[i], value)
			}
			fmt.Println()
		}
	}

	if err = rows.Err(); err != nil {
		return fmt.Errorf("error during row iteration: %v", err)
	}

	return nil
}

func main() {
	inputJson := flag.String("i", "", "Input JSON file for connection details")
	outputGob := flag.String("o", "", "Output GOB file for connection details")
	connectionGob := flag.String("c", "", "GOB file to use for database connection")
	queryStr := flag.String("q", "", "SQL query to execute")
	queryFile := flag.String("f", "", "SQL file containing query to execute")
	asCSV := flag.Bool("csv", false, "Output results as CSV (only for SELECT statements)")

	flag.Parse()

	if *inputJson != "" && *outputGob != "" {
		err := CreateConnection(*inputJson, *outputGob)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	} else if *connectionGob != "" {
		if (*queryStr != "" && *queryFile != "") || (*queryStr == "" && *queryFile == "") {
			fmt.Fprintf(os.Stderr, "Error: You must provide EITHER -q or -f for the query.\n")
			os.Exit(1)
		}

		err := QueryDatabase(*connectionGob, *queryStr, *queryFile, *asCSV)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	} else {
		fmt.Println("Usage:")
		fmt.Println("  Create connection gob file:")
		fmt.Println("    -i <input.json> -o <output.gob>")
		fmt.Println("  Query database:")
		fmt.Println("    -c <connection.gob> [-q <query> | -f <query_file>] [-csv]")
		flag.PrintDefaults()
	}
}
