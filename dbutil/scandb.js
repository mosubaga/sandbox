const mysql   = require('mysql');
const request = require('request');
const fs      = require('fs');
const http    = require('http');
const express = require('express');
const app     = express();

const con = mysql.createConnection({
  host: "[HOST]",
  user: "[USERNAME]",
  password: "[PASSWD]",
  database: "[DBNAME]"
});

// --------------------------------------------------------------------------------------
function FetchDB()
// --------------------------------------------------------------------------------------
{
    return new Promise(function(resolve, reject)
    {
        con.connect((err)=>{
            if (err){
                reject(err);
            }
            else
            {
                console.log("Connected to DB\n");
                let sCmd="[SQL STATEMENT]";
                con.query(sCmd, (err, result)=> {
                    if (err) throw err;
                    let rows = result.filter(function(row){
                        return row.content_url_path.length > 64000;
                    });
                    resolve(rows);
                });
                console.log("Closing DB\n");
                con.end();
            }
        });
    });
}

// --------------------------------------------------------------------------------------
function sBuildString(rows)
// --------------------------------------------------------------------------------------
{
    let sOutput = "<tr><th>Content</th><th>Key</th></tr>\n";
    for (i in rows){
        sOutput += "<tr><td>" + rows[i].context_row + "</td><td>"+ rows[i].content_orw + "</td></tr>\n";
    }
    return sOutput;
}

// --------------------------------------------------------------------------------------
function main()
// --------------------------------------------------------------------------------------
{
    app.get("/",function(req,response)
    {
        response.setHeader('Content-Type', 'text/html;charset=utf-8');
        response.write("<!DOCTYPE html>\n");
        response.write("<html lang=\"en\">\n<head>\n");
        response.write("<title>List</title>\n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\">\n</head>\n<body>\n<table id =\"myTable\" class=\"table table-hover\">\n");

        var initializePromise = FetchDB();
        initializePromise.then(function(result)
        {
           var sOutput = sBuildString(result);
           response.write(sOutput);
        }, function(err)
        {
            console.log(err);
        }).then(() =>
        {
            response.write("</table>\n</body>\n</html>");
            response.end();
        });
    });

    app.listen(9000,function(error)
    {
        if(error==true){
            console.log("error occured");
        }
        else
        {
            console.log("listening to localhost: 9000");
        }
    });
}

main();
