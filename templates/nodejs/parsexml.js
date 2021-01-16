const DOMParser = require('xmldom').DOMParser;
const fs = require('fs');

async function GenReport(string, type)
{
    const sFilePath = "[PATH]";
    const aFileList = walk(sFilePath);

    let count = 0;
    aFileList.forEach(await function (sFile) {
        fs.readFile(sFile, 'utf-8', function(err,data){
            const doc = new DOMParser().parseFromString(data, 'application/xml');
            const testsuite = doc.getElementsByTagName([some_tag_name]);
            const testcases = doc.getElementsByTagName([some_another_tag]);
            for (let x=0;x<testcases.length-1;x++){
                const failures = testcases[x].childNodes;
                if (failures.length > 1){
                    for (let i=0;i<failures.length;i++) {
                        if (failures[i].nodeName == '[some_key]') {
                            count++;
                            console.log(`---------------------------------- (${count}) ----------------------------------------`);
                            console.log("TEXT" + testsuite[0].getAttribute('[some_text]'));
                        }
                    }
                }
            }
        });
    })
}

var walk = function(dir) {
    var results = []
    var list = fs.readdirSync(dir)
    list.forEach(function(file) {
        file = dir + '/' + file
        var stat = fs.statSync(file)
        if (stat && stat.isDirectory()) results = results.concat(walk(file))
        else results.push(file)
    })
    return results
}

GenReport();


