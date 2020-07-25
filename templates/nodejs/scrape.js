const axios = require('axios');
const cheerio   = require('cheerio');

const sURL  = "[URL]";

function GetContetnt(sURL) {

    const config = {
        method: 'get',
        url: sURL,
        headers: { 'User-Agent': 'Chrome/35.0.1916.47' }
    }

    const resp = axios(config);
    resp
    .then(result => console.log(`Got Content for ${sURL}`))
    .catch(error => console.error('(1) Inside error:', error))
    return resp;
}

GetContetnt(sURL)
.then((response)=>{
    let text = response.data;
    let $ = cheerio.load(text);
    $("a").each((i, link)=>{
        sHref = $(link).attr("href")
        if (sHref != undefined){
            if (sHref.startsWith("[URL]"))
            {
                console.log(sHref);
            }
        }
    });
});
