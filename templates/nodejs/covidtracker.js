const http = require('http');
const axios = require('axios');
const express = require('express');

const app = express();
console.log("Starting server on port : 2349");

function GetJSON(sURL) {
    const resp = axios.get(sURL);
    resp
        .then(result => console.log(`Got JSON for ${sURL}`))
        .catch(error => console.error('(1) Inside error:', error))
    return resp;
}

function PrintHeader(sTitle) {
    let sHeader = "<!DOCTYPE html>\n";
    sHeader += "<html>\n";
    sHeader += "<head>\n";
    sHeader += `<title>${sTitle}</title>\n`;
    sHeader += "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\">\n";
    sHeader += "</head>\n<body>\n"
    return sHeader;
}

app.get("/", (request,response) => {
    response.write("Covid tracker amongst regions");
    response.end();
});

app.get("/USAStates", (reqest,response) =>{
    response.write('<table><tr><th>State</th><th>Cases</th><th>Deaths</th></tr>');
    GetJSON("https://covid19-server.chrismichael.now.sh/api/v1/CasesInAllUSStates")
        .then((result) => {
            response.write(PrintHeader("Cases in USA States"))
            result.data.data[0].table.forEach((item) =>{
                response.write(`<tr><td>${item['USAState']}</td><td>${item['TotalCases']}</td><td>${item['TotalDeaths']}</td></tr>`);
            });
        })
        .then(()=>{
            response.write("\n</table>\n</body>\n</html>\n");
            response.end();
        })
        .catch((error) => {
            console.log(error);
        })
});

app.get("/Europe", (reqest,response) =>{
    response.write('<table><tr><th>Nation</th><th>Cases</th><th>Deaths</th></tr>');
    GetJSON("https://covid19-server.chrismichael.now.sh/api/v1/AllCasesInEurope")
        .then((result) => {
            response.write(PrintHeader("Cases in Europe"))
            result.data.data[0].table[0].forEach((item) =>{
                response.write(`<tr><td>${item['Country']}</td><td>${item['Cases']}</td><td>${item['Deaths']}</td></tr>`);
            });
        })
        .then(()=>{
            response.write("\n</table>\n</body>\n</html>\n");
            response.end();
        })
        .catch((error) => {
            console.log(error);
        })
});

app.listen(2349,function(error){
    if(error==true){
        console.log("Error in the server ...");
    }else{
        console.log("Listening to localhost:2349");
    }
});

