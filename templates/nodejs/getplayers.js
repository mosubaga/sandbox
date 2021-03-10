const axios       = require('axios');
const cheerio     = require('cheerio');
const fs          = require('fs');
const writeStream = fs.createWriteStream('[sCSVFile]');

const sURLRoot='[sURL]';

// -----------------------------------------------
function GetContent(sURLRoot) 
// -----------------------------------------------
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

// -----------------------------------------------
function CleanString(text)
// -----------------------------------------------
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

// -----------------------------------------------
function GetTeam(sText){
// -----------------------------------------------

    let regex1 = /<.*?>/g;
    let sOut = sText.replace(regex1,"");

    let regex2 = /^(.)(.+)/;
    match = regex2.exec(sOut);

    return `,${match[1]}`;
}

// -----------------------------------------------
function main()
// -----------------------------------------------
{
        GetContent(sURLRoot)
            .then((response) => {
                let text = response.data;
                let $ = cheerio.load(text);

                const aIndex = [4,6,8,10,12,14,16,18,20,22,24,26,28];

                aIndex.forEach(iIndex => {

                    let sRootElem = `#content > section > article > div > table:nth-child(${iIndex}) > tbody > tr:nth-child(1) > td`;

                    let sTeamName = $(sRootElem);
                    let sCleanedTeamName = GetTeam(sTeamName.text());

                    for (x=3; x<15; x++) {
                        let sSelector = `#content > section > article > div > table:nth-child(${iIndex}) > tbody > tr:nth-child(${x})`

                        let elem = $(sSelector);
                        const sPlayer = CleanString(elem.html()) + sCleanedTeamName;

                        console.log(sPlayer);
                        writeStream.write(`${sPlayer}\n`)
                    }
                });
            });
}

main();