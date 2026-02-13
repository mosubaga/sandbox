package main

import (
	"context"
	"database/sql"
	"fmt"
	"html"
	"log"
	"os"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// Global inputs for database access.
var (
	hostname     = "localhost"
	username     = "username"
	password     = "password"
	databaseName = "database_name"
)

// Put your SQL statements in this array.
var queries = []string{
	"select * from table_01;",
	"select * from table_02;",
	"select * from table_03;",
}

func main() {
	if err := run(); err != nil {
		log.Printf("cgi error: %v", err)
		printCGIHeader()
		fmt.Println("<html><body>")
		fmt.Printf("<h2>Error</h2><pre>%s</pre>", html.EscapeString(err.Error()))
		fmt.Println("</body></html>")
		os.Exit(1)
	}
}

func run() error {
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?parseTime=true", username, password, hostname, databaseName)
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return fmt.Errorf("open database: %w", err)
	}
	defer db.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := db.PingContext(ctx); err != nil {
		return fmt.Errorf("ping database: %w", err)
	}

	printCGIHeader()
	fmt.Println("<html><head><title>Query Results</title></head><body>")
	fmt.Println("<h1>MySQL Query Results</h1>")

	for _, q := range queries {
		// fmt.Printf("<h2>Statement %d</h2>\n", i+1)
		fmt.Printf("<pre>%s</pre>\n", html.EscapeString(q))

		if err := renderQueryResult(ctx, db, q); err != nil {
			fmt.Printf("<p><strong>Error:</strong> %s</p>\n", html.EscapeString(err.Error()))
		}
	}

	fmt.Println("</body></html>")
	return nil
}

func printCGIHeader() {
	fmt.Print("Content-Type: text/html\r\n\r\n")
}

func renderQueryResult(ctx context.Context, db *sql.DB, query string) error {
	rows, err := db.QueryContext(ctx, query)
	if err != nil {
		res, execErr := db.ExecContext(ctx, query)
		if execErr != nil {
			return fmt.Errorf("query failed: %w", err)
		}

		affected, affErr := res.RowsAffected()
		if affErr != nil {
			affected = 0
		}
		fmt.Printf("<p>Statement executed. Rows affected: %d</p>\n", affected)
		return nil
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		return fmt.Errorf("read columns: %w", err)
	}

	fmt.Println("<table border=\"1\" cellpadding=\"6\" cellspacing=\"0\">")
	fmt.Println("<tr>")
	for _, col := range columns {
		fmt.Printf("<th>%s</th>", html.EscapeString(col))
	}
	fmt.Println("</tr>")

	for rows.Next() {
		values := make([]any, len(columns))
		valuePtrs := make([]any, len(columns))
		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			return fmt.Errorf("scan row: %w", err)
		}

		fmt.Println("<tr>")
		for _, v := range values {
			fmt.Printf("<td>%s</td>", html.EscapeString(cellToString(v)))
		}
		fmt.Println("</tr>")
	}

	if err := rows.Err(); err != nil {
		return fmt.Errorf("iterate rows: %w", err)
	}

	fmt.Println("</table>")
	return nil
}

func cellToString(v any) string {
	if v == nil {
		return "NULL"
	}

	switch t := v.(type) {
	case []byte:
		return string(t)
	case time.Time:
		return t.Format(time.RFC3339)
	default:
		return strings.TrimSpace(fmt.Sprint(t))
	}
}
