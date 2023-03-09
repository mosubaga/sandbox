import asyncio,time
from playwright.async_api import async_playwright,expect

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("[URL]")
        await page.wait_for_load_state('networkidle')

        
        await page.locator("[Selector1]").fill(username)
        await page.locator("[Selector2]").click()

        await page.locator("[Selector3]").fill(passwd)
        await page.locator("[Selector2]").click()

        await expect(page.locator('[Selector5]')).to_be_visible()
        stext = await page.locator('[Selector6]').inner_text()
        print(stext)

        print(await page.title())

        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url, response.headers))

        await browser.close()


asyncio.run(main())
