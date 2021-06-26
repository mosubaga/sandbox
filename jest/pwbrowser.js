const {chromium, firefox} = require('playwright');
const assert = require('assert');

async function main()
{
	
	for (const browserType of [chromium, firefox])
	{
  		console.log(`Running on ${browserType.name()}`)
  		const browser = await browserType.launch({headless : false});
  		const page = await browser.newPage();
  		await page.goto('[sURL]', {waitUntil: 'networkidle'});

  		const lt = await page.$$eval('[sSelector]', lists =>
    		lists.map(link => link.getAttribute('[sID]'))
  		)

  		const st = await page.$$eval('[sSelector]', lists =>
    		lists.map(link => link.textContent)
  		)		

  		assert.equal(st.length,lt.length,"Test Failed (1)");
  		await browser.close();
	}
}

main();
