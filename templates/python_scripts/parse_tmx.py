from lxml import etree

import sys
import shutil
import os
import re
import io
import codecs

# ------------------------------------------------------------------------------

def parseTMX(xml_file):

    src_txt = ""
    tgt_txt = ""

    f = codecs.open("tmx_txt_fr.txt", "w", encoding="utf-8")
    f.write(u'\ufeff')

    for event, element in etree.iterparse(xml_file,events=("start", "end")):
        if event == 'start' and element.tag =='tuv':
            lang_dict = element.attrib
            test_lang = lang_dict['{http://www.w3.org/XML/1998/namespace}lang']
            children = element.getchildren()
            lang = str(element.attrib)
            for child in children:
                segment = etree.tostring(child,encoding="utf-8")
                segment = segment.decode("utf-8")
                segment = segment.replace("<seg>","")
                segment = segment.replace("</seg>","")
                segment = segment.replace("&gt;",">")
                segment = segment.replace("&lt;","<")
                segment = segment.replace("&amp;","&")
                segment = re.sub("<ph.*?\>","",segment)
                segment = re.sub("<ut>.*?</ut>","",segment)
                segment = re.sub("<.*?>","",segment)
                segment = re.sub("{\\\\.+}","",segment)
                segment = segment.rstrip()

                if not segment == '' and not segment == '<seg/>':
                    if re.search("ja-JP",lang,re.IGNORECASE):
                        f.write("SRC:" + segment +"\r\n")
                    else:
                        f.write(test_lang + ": " + segment +"\r\n")

    f.close()

# ------------------------------------------------------------------------------


def main():
    parseTMX('fr_test.tmx')
    print "++ Finished Extraction ++"

if __name__ == '__main__':
    main()