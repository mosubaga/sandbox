import sys
import shutil
import os
import re
import pprint
import codecs

# ------------------------------------------------------------------------------

def test_encode(input):

    fh  = codecs.open(input, 'r', 'euc-jp')
    out = codecs.open("py_utf8.txt", 'w', 'utf8')

    for line in fh:
        line = line.encode("utf8")
        line = line.decode("utf8")
        out.write(line)

    fh.close()
    out.close()

# ------------------------------------------------------------------------------

def main():
   input = "py.txt"
   test_encode(input)

if __name__ == '__main__':
   main()