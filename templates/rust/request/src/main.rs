extern crate reqwest;
use serde_json::Value;

fn main(){

    let resp = match reqwest::blocking::get("[URL]") {
        Ok(resp) => resp.text().unwrap(),
        Err(err) => panic!("Error: {}", err)
    };

    // Parse the string of data into serde_json::Value.
    let json_data: Value = match serde_json::from_str(&resp) {
        Ok(v) => v,
        Err(err) => panic!("Error: {}", err)
    };

    println!("Version of app: {}",  json_data["[FIELD]"]);
}
