const webdriver = require('selenium-webdriver');

// --------------------------------------------------
async function TestGoogle()
// --------------------------------------------------
{
	const browser = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
	await browser.get('https://www.google.com/');
	
	let promise = browser.getTitle();	
	promise.then((title)=>{
		console.log(title);
	}).then(()=>{
		browser.quit();
		console.log("== Test Complete ==");
	}).catch(()=>{
		console.log("== Error in test ==");
	});

	// browser.quit();
	// console.log("== Test Complete ==");
}

// --------------------------------------------------
async function TestGoogleSearch()
// --------------------------------------------------
{	
	const driver = await new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
		
	try
	{
		await driver.get('https://www.google.com/');
	
		let element = await driver.findElement(webdriver.By.name('q'));
    	await element.sendKeys('webdriver');
    	await console.log("== Submit form ==");
    	await element.submit();
    	
    	await driver.wait(webdriver.until.elementLocated(webdriver.By.className("LC20lb")), 10000);
    	
    	let sTitle = await driver.getTitle();
    	console.log(sTitle);
    	await driver.quit();
    	await console.log("== Test Complete ==");
	}
	catch(err)
	{
    	console.error('Exception!\n', err.stack, '\n');
        driver.quit();
    }
}

TestGoogleSearch();
