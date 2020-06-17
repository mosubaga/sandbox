# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import aiofiles
import os, re, json,pprint


async def download_html(session, url):
    async with session.get(url, ssl=False) as res:
        aURI = re.split('\.', url)
        filename = f'{aURI[1]}.txt'

        async with aiofiles.open(filename, 'wb') as f:
            while True:
                chunk = await res.content.read()
                if not chunk:
                    break
                await f.write(chunk)

        return await res.release()


async def requrl(url):
    async with aiohttp.ClientSession() as session:
        await download_html(session, url)


def main():
    urls = ['URL1','URL2']
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*(requrl(url) for url in urls)))

if __name__ == '__main__':
    main()