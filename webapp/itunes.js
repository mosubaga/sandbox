const axios      = require('axios');
const http       = require('http');
const express    = require('express');

const app        = express();
const sURL  = "https://itunes.apple.com/lookup?id=136975";

function GetJSON(sURL) {
    const resp = axios.get(sURL);
    resp
    .then(result => console.log(`Got JSON for ${sURL}`))
    .catch(error => console.error('(1) Inside error:', error))
    return resp;
}

function PrintHeader(sTitle) {
    sHeader = "<!DOCTYPE html>\n";
    sHeader += "<html>\n";
    sHeader += "<head>\n";
    sHeader += `<title>${sTitle}</title>\n`;
    sHeader += "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\">\n";
    sHeader += "</head>\n<body>\n"
    return sHeader;
}

app.get("/", (request,response) => {
    response.write("Search Result");
    response.end();
});

app.get("/Album", (reqest,response) =>{
    GetJSON(sURL + "&entity=album")
    .then((result) => {
        response.write(PrintHeader("Album List"))
        result.data.results.forEach((album) =>{
            if (album.collectionName != undefined){
                response.write(`<p><img src="${album.artworkUrl60}"></img>&nbsp;<strong>${album.collectionName}</strong></p>\n`);
            }        
        });
    })
    .then(()=>{
        response.write("\n</body>\n</html>\n");
        response.end();
    })
    .catch((error) => {
        console.log(error);
    })
});

app.get("/Song", (reqest,response) =>{
    GetJSON(sURL + "&entity=song&limit=100")
    .then((result) => {
        response.write(PrintHeader("Songs"))
        result.data.results.forEach((song) =>{
            if (song.trackName != undefined){
                response.write(`<p><img src="${song.artworkUrl60}"></img>&nbsp;<strong>${song.trackName}</strong></p>\n`);
            }        
        });
    })
    .then(()=>{
        response.write("\n</body>\n</html>\n");
        response.end();
    })
    .catch((error) => {
        console.log(error);
    })
});

app.listen(2349,function(error){
    if(error==true){
        console.log("error occured");
    }else{
        console.log("listening to localhost:2349");
    }
});
