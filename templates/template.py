import sys, shutil, os, re, codecs, pprint

# ------ 

def function():
	pass

def list_file(root_dir):

    obj = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xxx') or file.endswith('.yyy'):
              	full_obj = os.path.join(root,file)
                obj.append(full_obj)

    return obj


# ------

def main():
	pass

if __name__ == '__main__':
    main()
