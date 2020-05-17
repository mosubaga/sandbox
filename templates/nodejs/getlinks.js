var request = require('request');
var cheerio = require('cheerio');

const g_UrlRoot='[URL]';

function main() 
{
    request(g_UrlRoot, (err, resp, body) => {
        if (!err && resp.statusCode == 200) 
        {
            $ = cheerio.load(body);

            $('li').each((index,value) => {
                let link = $(value).children().text();
                let text = $(value).children().attr('href');
                console.log(link + " : " + text);
        });
        }
    });
}

main();