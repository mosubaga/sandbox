from xml.dom import minidom

import sys
import shutil
import os
import re
import io
import codecs
import pprint

# ------------------------------------------------------------------------------

def ParseRESX(resx_file):

    txt_file = resx_file
    txt_file = txt_file.replace(".resx",".txt")
    fh = codecs.open(txt_file, "w", encoding="utf-8")

    xmldoc = minidom.parse(resx_file)
    nodes  = xmldoc.getElementsByTagName('data')

    for node in nodes:
      if node.hasChildNodes():
        res_id = node.getAttribute('name')
        children = node.childNodes
        for child in children:
          if (child.nodeName == 'comment'):
            fh.writelines(res_id + "="+child.firstChild.nodeValue+"\n")

    fh.close()

# ------------------------------------------------------------------------------

def ReadTXT(txt_file):

    fh = codecs.open(txt_file, "r", encoding="utf-8")
    data_dict = {}

    for line in fh:
      if re.search('^(.+?)=(.+?)$',line):
        resid=re.search('^(.+?)=(.+?)$',line).group(1)
        value=re.search('^(.+?)=(.+?)$',line).group(2)
        data_dict[resid]=value
    fh.close()

    return data_dict

# ------------------------------------------------------------------------------

def ModResx(txt_file,data_dict):

    resx_file = txt_file
    resx_file = resx_file.replace(".txt",".resx")

    xmldoc = minidom.parse(resx_file)
    nodes  = xmldoc.getElementsByTagName('data')

    for node in nodes:
      if node.hasChildNodes():
        res_id = node.getAttribute('name')
        children = node.childNodes
        for child in children:
          if (child.nodeName == 'comment'):
            child.firstChild.nodeValue = data_dict[res_id]

    fh = open("dummy.xml","wb")
    xmldoc.writexml(fh,encoding='utf-8')
    xmldoc.unlink()
    fh.close()

    os.rename(resx_file,resx_file + '.orig')
    os.rename("dummy.xml",resx_file)

# ------------------------------------------------------------------------------


def main():

   mode = sys.argv[1]

   if (mode == 'extract'):
      ParseRESX('Whatever.resx')
   elif (mode == 'update'):
     txt_file = 'Whatever.txt'
     data_dict = ReadTXT(txt_file)
     ModResx(txt_file,data_dict)
   else:
     print("Unknown mode")


if __name__ == '__main__':
    main()
