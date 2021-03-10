const axios       = require('axios');
const cheerio     = require('cheerio');
const fs          = require('fs');

const writeStream = fs.createWriteStream('[sCSVFile]');
const sURLRoot='[SURL]';

// ----------------------------------------------
function GetContent(sURLRoot) 
// ----------------------------------------------
{

    const config = {
        method: 'get',
        url: sURLRoot,
        headers: { 'User-Agent': 'Chrome/35.0.1916.47' }
    }

    const resp = axios(config);
    resp
        .then(result => console.log(`Got Content for ${sURLRoot}`))
        .catch(error => console.error('(1) Inside error:', error))
    return resp;
}

// ----------------------------------------------
function CleanString(text)
// ----------------------------------------------
{
    let regex = /<.*?>/g;
    let sOut = text.replace(regex,"");

    aLines = sOut.split("\n");

    let sPlayer = "";
    for (j=1;j<aLines.length-1;j++){
        if (j < aLines.length-2){
            sPlayer += aLines[j].trim() + ",";
        }
        else{
            sPlayer += aLines[j].trim();
        }
    }

    return sPlayer;
}

// ----------------------------------------------
function main()
// ----------------------------------------------
{
    GetContent(sURLRoot)
        .then((response) => {
            let text = response.data;
            let $ = cheerio.load(text);

            const aIndex = [5,7,9,11,13,15,17,18,19,21,23,25,27,29];

            aIndex.forEach(iIndex => {

                let sRootElem = `#content > section > article > div > table:nth-child(${iIndex}) > tbody`;

                for (x=2; x<6; x++) {
                    let sSelector = `#content > section > article > div > table:nth-child(${iIndex}) > tbody > tr:nth-child(${x})`;

                    let elem = $(sSelector);
                    const sPlayer = CleanString(elem.html());

                    console.log(sPlayer);
                    writeStream.write(`${sPlayer}\n`);
                }
            });
        });
}

main();