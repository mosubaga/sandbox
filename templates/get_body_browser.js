const webdriver = require('selenium-webdriver');
const fs        = require('fs');
const assert    = require('assert');

const sSrcURL = "https://www.google.com";
const sTgtURL = "https://www.google.co.jp";

// --------------------------------------------------
async function GetContent(sURL,sBrowser)
// --------------------------------------------------
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
}

async function TestBrowserChrome()
{
    sSrcText = await GetContent(sSrcURL,"chrome");
    sTgtText = await GetContent(sTgtURL,"chrome");
    assert(sSrcText != sTgtText, "Test failed: The content should not be equal on Chrome.");
}

async function TestBrowserIe11()
{
    sSrcText = await GetContent(sSrcURL,"ie11");
    sTgtText = await GetContent(sTgtURL,"ie11");
    assert(sSrcText != sTgtText, "Test failed: The content should not be equal on IE11");
}

async function TestBrowserFirefox()
{
    sSrcText = await GetContent(sSrcURL,"firefox");
    sTgtText = await GetContent(sTgtURL,"firefox");
    assert.notEqual(sSrcText,sTgtText,"Test failed: The content should not be equal on Firefox");
}

// --------------------------------------------------
async function runtest(sTestName, callback)
// --------------------------------------------------
{
    let startTime = new Date();
    let TstartTime = await startTime.getHours() + ":" + startTime.getMinutes() + ":" + startTime.getSeconds();
    await console.log("== Start Testing " + TstartTime + " " + sTestName + " ==");

    await callback();

    let endTime = new Date();
    let TendTime = await endTime.getHours() + ":" + endTime.getMinutes() + ":" + endTime.getSeconds();
    await console.log("== End Testing " + TendTime + " " + sTestName + " ==\n");
}

// --------------------------------------------------
async function main()
// --------------------------------------------------
{
    await runtest("TestBrowserChrome", TestBrowserChrome);
    await runtest("TestBrowserFirefox",TestBrowserFirefox);
    await runtest("TestBrowserIe11", TestBrowserIe11);
}

main();
