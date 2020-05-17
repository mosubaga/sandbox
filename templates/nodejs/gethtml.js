
const cheerio = require('cheerio');
const request = require('request');

function getData() {

    let url="https://cheerio.js.org/";

    const item=[];
    request(url, function(error, response, html) {
        if(!error) {
            const $ = cheerio.load(html);
            $('h4').each(function(i, elem) {
                item[i] = $(this).text();
                console.log(item[i]);
              });
        }
        else{
            console.log("ERROR")
        }
    });
}

getData()