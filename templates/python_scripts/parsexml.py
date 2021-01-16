import sys, shutil, os, re, codecs, datetime
from xml.dom import minidom

def list_file(sRootDir):

    obj = []
    for root, dirs, files in os.walk(sRootDir):
        for file in files:
            if file.endswith('.xml'):
                full_obj = os.path.join(root,file)
                obj.append(full_obj)
    return obj

def createReport():

    x = datetime.datetime.now()
    sCwd = os.getcwd()
    sRootDir    = sCwd + "[some_folder]"
    print(sRootDir)
    aReportList = list_file(sRootDir)

    oFH = codecs.open("summary.txt","w",encoding="utf8")
    oFH.write(str(x) + "\n")
    count = 0
    for sReport in aReportList:
        sLog = ""
        doc = minidom.parse(sReport)
        testsuites = doc.getElementsByTagName("[some_tag]")
        for testsuite in testsuites:
            if testsuite.hasChildNodes():
                testcases = testsuite.getElementsByTagName("[another_tag]")
                for testcase in testcases:
                    failures = testcase.getElementsByTagName("[just_another_tag]")
                    for failure in failures:
                        sLog += "---------------------------------------------------------------\n"
                        sLog += testsuite.getAttribute("[att_name]") + "\n"
                        sLog += testcase.getAttribute("[some_att_name]") + "\n"
                        sLog += failure.getAttribute("[some_another_att_name]") + "\n"
                        sLog += failure.firstChild.data + "\n"
                        count += 1
        oFH.write(sLog)
    oFH.write("---------------------------------------------------------------\n")
    oFH.write("Total: " + str(count))
    oFH.close()

# ------------------------------------------------------------------------------

def main():
    createReport()
    print(":: Done ::")

if __name__ == '__main__':
    main()
