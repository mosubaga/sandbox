var http = require('http');
var fs = require('fs');
var bodyParser = require('body-parser');

const express = require('express');
const app = express();

app.use("/",express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({extended : true}));

app.get("/",function(request,response){
    response.setHeader('Content-Type', 'text/html');
    var data = fs.readFileSync('search.html', 'utf8');
	response.write(data)
    response.end(); //end the response
 });

 app.post("/search",function(request,response){

    var keyword  = request.body.find;
    var root_dir = "<root_dir>";
    var files    = walk(root_dir);
    var match    = /^.*\.(java)$/;
    var i        = 0;

    response.setHeader('Content-Type', 'text/html');
    response.write("<!DOCTYPE html>\n");
    response.write("<html lang=\"en\">\n");
    response.write("<head>\n");
    response.write("<title>Search Tool</title>\n");
    response.write("<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\">\n");
    response.write("</head>\n");
    response.write("<body>\n");
    response.write('<b>Found following:</b><br><br>\n');
    response.write("<table id =\"myTable\" class=\"table table-hover\">");
    response.write("<tr><th>File</th><th>No.</th><th>Line</th></tr>");

    for (var x in files){
        if (match.test(files[x])){
           var j = 1;
           var lines = fs.readFileSync(files[x]).toString().split('\n');
           for (var k = 0, len = lines.length; k < len; k++) {
             if (lines[k].match(keyword)){
                 files[x] = files[x].replace(root_dir,"");
                 response.write("<tr><td>" + files[x] + "</td><td>" + j + "</td><td>" + lines[k] + "</td></tr>");
                 i++;
             }
             j++;
           }
        }
     }

    response.write("</table>");
    response.write("<br><b>Found " + i + " hits</b>\n");
    response.write("</body>\n");
    response.write("</html>\n");
    response.end();
 });

 app.listen(9000,function(error){
    if(error==true){
        console.log("error occured") 
    }else{
        console.log("listening to localhost:9000")
    }
})

var walk = function(dir) {
    var results = []
    var list = fs.readdirSync(dir)
    list.forEach(function(file) {
    	// console.log(file)
        file = dir + '/' + file
        var stat = fs.statSync(file)
        if (stat && stat.isDirectory()) results = results.concat(walk(file))
        else results.push(file)
    })
    return results
}