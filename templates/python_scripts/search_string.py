import sys, shutil, os, re, codecs, pprint

def scan_dir(root_dir):

    filelist =[]

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                full_obj = os.path.join(root, file)
                filelist.append(full_obj)

    return filelist

def readfiles(sfile):

    for line in codecs.open(sfile,'r',encoding='utf8'):
        yield line

def grep(pattern, lines):

    return (line for line in lines if pattern in line)

def printlines(lines):

    for line in lines:
        print(line.lstrip().rstrip(), end="\n")

def search_string(pattern, filelist):

    for sfile in filelist:
        lines =readfiles(sfile)
        lines = grep(pattern, lines)
        for line in lines:
            print(sfile + ": " + line.strip())

def main(): 
    
    pattern = "[Keyword]"
    filelist = scan_dir(r'[FolderPath]')
    search_string(pattern, filelist)

if __name__ == '__main__':
    main()
