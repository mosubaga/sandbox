use mysql::prelude::*;
use mysql::*;

fn main() {
    // MySQL database connection details
    let url = "mysql://admin:gyoker@localhost:8889/megaten";

    // Establish a connection to the MySQL database
    let pool = Pool::new(url).expect("Failed to create MySQL connection pool");

    // Get a connection from the pool
    let mut conn = pool.get_conn().expect("Failed to get MySQL connection from pool");

    // Run a query
    let query = "select id, cname from nocturne where clevel > 89;";
    let result: Vec<(i32, String)> = conn.query_map(query, |(id, name)| (id, name)).expect("Failed to execute query");

    // Process the results
    for (id, name) in result {
        println!("ID: {}, Name: {}", id, name);
    }
}