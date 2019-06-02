import sys
import shutil
import os
import re
import pprint
import codecs
import csv
import math, operator
from PIL import Image  # in pillow or PIL

# ------------------------------------------------------------------------------

def read_csv(csv_file):
  with open(csv_file,'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      print(row[3])

# ------------------------------------------------------------------------------

def main():
  csv_file = r'<CSV File Name>'
  read_csv(csv_file)

if __name__ == '__main__':
    main()
