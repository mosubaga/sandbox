const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();

// app.use(express.static('staging'))

app.use("/",express.static(__dirname));

app.get("/",function(request,response){
    response.setHeader('Content-Type', 'text/html');
    response.sendFile(path.join(__dirname + '/index.html'));
});


app.listen(9090,function(error){
    if(error==true){
        console.log("error occured");
    }else{
        console.log("=========================================");
        console.log(":: Root directory is : " + __dirname);
        console.log(":: Listening to localhost:9090");
        console.log("=========================================");
    }
});

