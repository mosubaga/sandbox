//////////////////////////////////////////////////////////////////////////
const DOMParser = require('xmldom').DOMParser;
const fs = require('fs');
const oDate = new Date();
const sReportName = "[filename]"
//////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////
function GenReport()
/////////////////////////////////////////////////////////////////////////
{

   let bGotTestResult = new Promise(resolve=> {
     const aFileList = walk(__dirname.concat("[folder]"));
     resolve(aFileList)
   });

   bGotTestResult
   .then((aFileList)=>{

     // Start building summary
     let sContent = `Failures recorded as of : ${oDate.getMonth()+1}/${oDate.getDate()}/${oDate.getYear()+1900}` + "\n";
     let count =  0;

     for (let i = 0; i < aFileList.length; i++) {
       if (GetError(aFileList[i])!= "NoErrMsg"){
          sContent += GetError(aFileList[i])
          count++;
        }
     }

     sContent +="------------------------------------------------------------------------\n";
     sContent += `Total of ${count} error(s)`;

     return sContent;
   })
   .then((sTestResult) => {
      // Paste summary on text file
      fs.writeFileSync(sReportName,sTestResult);
      console.log(`:: ${oDate.getHours()}:${oDate.getMinutes()}:${oDate.getSeconds()} :: Created report  : ${sReportName}`);
    })
}

/////////////////////////////////////////////////////////////////////////
function GetError(sXMLFile)
/////////////////////////////////////////////////////////////////////////
{
  let sErrMsg = "";
  const data = fs.readFileSync(sXMLFile, {encoding:'utf8', flag:'r'});
  const doc = new DOMParser().parseFromString(data, 'application/xml');
  const testsuite = doc.getElementsByTagName('testsuite');
  const testcases = doc.getElementsByTagName('testcase');
  for (let x=0;x<testcases.length-1;x++){
      const failures = testcases[x].childNodes;
      if (failures.length > 1){
          for (let i=0;i<failures.length;i++) {
              if (failures[i].nodeName === 'failure') {
                  sErrMsg += "------------------------------------------------------------------------\n";
                  sErrMsg += "Test Suite: " + testsuite[0].getAttribute('name') + "\n";
                  sErrMsg += "Test Case: " + testcases[x].getAttribute('name') + "\n"
                  sErrMsg += "Failure Message: " + failures[i].getAttribute('message') + "\n";
                  sErrMsg += "Failure Details: \n" + failures[i].firstChild.nodeValue + "\n";
                  return sErrMsg;
              }
          }
      }
  }

  return "NoErrMsg";
}

const walk = function(dir) {
    let results = []
    const list = fs.readdirSync(dir)
    list.forEach(function(file) {
        file = dir + '/' + file
        const stat = fs.statSync(file)
        if (stat && stat.isDirectory()) results = results.concat(walk(file))
        else results.push(file)
    })
    return results
}

// --- main() here --- //

fs.exists(sReportName, function(exists) {
  if(exists) {
    console.log(`:: ${oDate.getHours()}:${oDate.getMinutes()}:${oDate.getSeconds()} :: Deleting report : ${sReportName}`);
    fs.unlinkSync(sReportName);
    GenReport();
  }
  else{
    GenReport();
  }
});

// GenReport();
