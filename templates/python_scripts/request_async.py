# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import aiofiles
import os, re, json,pprint


async def download_html(session, url):
    async with session.get(url, ssl=False) as res:
        aURI = re.split('\/', url)
        filename = f'{aURI[4]}.json'

        async with aiofiles.open(filename, 'wb') as f:
            while True:
                chunk = await res.content.read()
                if not chunk:
                    break
                await f.write(chunk)

        return await res.release()


async def main(url):
    async with aiohttp.ClientSession() as session:
        await download_html(session, url)


urls = [
    '[API_URL1]',
    '[API_URL2]'
]

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(*(main(url) for url in urls))
)
