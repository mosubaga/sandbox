import sys
import shutil
import os
import re

################################################################################
root_dir = "<rootDir>"
################################################################################

# ------------------------------------------------------------------------------

def list_file(root_dir):

    lang = sys.argv[1]
    pattern = '[german|french|spanish|italian|swedish|finnish]'

    print "Copying for language: %s" % lang

    if re.match(pattern,lang):
        lang = 'euro'

    obj = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
    	   if file.endswith('.xxx') or file.endswith('.yyy') :
              full_obj = os.path.join(root,file)
              if lang in full_obj:
                obj.append(full_obj)

    return obj

# ------------------------------------------------------------------------------

def copy_files(obj):

    for obj_file in obj:
        o = os.path.basename(obj_file)
        tgt = root_dir + "\\" + o
        if os.path.isfile(tgt):
            os.remove(tgt)
        print "Copying %s to %s ... " % (obj_file,tgt)
        shutil.copy(obj_file,tgt)

# ------------------------------------------------------------------------------

def main():

    obj = []
    obj = list_file(root_dir)
    copy_files(obj)
    print "Finish copying ...\n"

if __name__ == '__main__':
    main()
