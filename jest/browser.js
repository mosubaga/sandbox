const webdriver = require('selenium-webdriver');
const fs        = require('fs');

// ---------------------------------------------------
async function GetContent(sURL, sBrowser)
// ---------------------------------------------------
{

    let driver;

    switch (sBrowser)
    {
        case 'chrome':
            driver = await new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
            break;
        case 'ie11':
            driver = await new webdriver.Builder().withCapabilities(webdriver.Capabilities.ie()).build();
            break;
        case 'firefox':
            driver = await new webdriver.Builder().withCapabilities(webdriver.Capabilities.firefox()).build();
            break;
        case 'edge':
            driver = await new webdriver.Builder().withCapabilities(webdriver.Capabilities.edge()).build();
            break;
        default:
            console.log("Error: Unable to assign the WebDriver.");
    }

    let sLogName = await sURL;
    sLogName = await sLogName.replace("https://","");
    sLogName = await sLogName.replace("http://","");
    sLogName = await sLogName.replace(/\./g,"");
    sLogName = await sLogName + "_" + sBrowser + ".log";

    await driver.get(sURL);

    try
    {
        await driver.wait(webdriver.until.elementLocated(webdriver.By.tagName("body"), 10000));
        let eBody = await driver.findElement(webdriver.By.tagName("body"));
        let sText = await eBody.getText();
        await driver.close();
        fs.writeFileSync(sLogName,sText);
        return sText;
    }
    catch(err)
    {
        console.error('Exception!\n', err.stack, '\n');
        driver.close();
    }

};

// ----------------------------------------------------
async function doescontentmatch()
// ----------------------------------------------------
{

    const sSrcURL   = "http://www.google.com";
    const sTgtURL   = "http://www.google.co.jp";
    const sBrowser  = "chrome";

    let sSrcContent = await GetContent(sSrcURL,sBrowser);
    let sTgtContent = await GetContent(sTgtURL,sBrowser);

    return await sSrcContent === sTgtContent;
}

module.exports = doescontentmatch

