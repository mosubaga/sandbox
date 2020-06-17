# -*- coding: utf-8 -*-
import sys, shutil, os, re, codecs, pprint
import asyncio
import aiofiles

def scan_dir(root_dir):

    filelist =[]

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.pl') or file.endswith('.js'):
                full_obj = os.path.join(root, file)
                filelist.append(full_obj)

    return filelist

async def search_string(pattern, sfile):

    i=1
    async with aiofiles.open(sfile, mode='r', encoding='utf8') as fh:
        lines = await fh.readlines()
        for line in lines:
            if pattern in line:
                print(sfile + " | line(" + str(i) + ") | " + line.strip())
            i+=1


def main(): 
    
    pattern = "[KEY]"
    filelist = scan_dir(r'[FOLDER]')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*(search_string(pattern, sfile) for sfile in filelist)))

if __name__ == '__main__':
    main()
