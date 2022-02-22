package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"log"
)

func main() {
	fmt.Println("Connecting to database ...")

	db, err := sql.Open("mysql", "dbuser:dbpassword@tcp(127.0.0.1:3306)/dbname")

	// if there is an error opening the connection, handle it
	if err != nil {
		panic(err.Error())
	}

	// defer the close till after the main function has finished
	// executing
	defer db.Close()

	// perform a db.Query insert
	df, err := db.Query("[SQL STATEMENT]")

	// if there is an error inserting, handle it
	if err != nil {
		panic(err.Error())
	}

	for df.Next() {
		var name string
		// for each row, scan the result into our tag composite object
		err = df.Scan(&name)
		if err != nil {
			panic(err.Error()) // proper error handling instead of panic in your app
		}
		// and then print out the row
		log.Printf(name)
	}

	// be careful deferring Queries if you are using transactions
	defer df.Close()
}
