# -*- coding: utf-8 -*-
import os, zipfile


def scan_dir(root_dir):
    azfiles = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.zip'):
                full_obj = os.path.join(root, file)
                azfiles.append(full_obj)

    return azfiles


def main():
    root_dir = r'[FILE_PATH]'
    azfiles = scan_dir(root_dir)
    for smodel in azfiles:
        stargetpath = os.path.dirname(smodel)
        with zipfile.ZipFile(smodel, "r") as zip_ref:
            zip_ref.extractall(stargetpath)

    print(":: Done ::")


if __name__ == '__main__':
    main()
