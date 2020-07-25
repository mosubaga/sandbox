import sys,pprint

import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

book = epub.read_epub(r'[EPUB]')

for x in book.toc:
    if type(x) == tuple:
        pprint.pprint(x[0].title)






