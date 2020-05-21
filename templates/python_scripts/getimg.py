from bs4 import BeautifulSoup
import sys, shutil, os, re, codecs, pprint
import urllib.request

# ------------------------------------------------------------------------------

def GetImages(base_url):
	for num in range(1,195):
		index = str(num)
		if num < 10:
			index = '00' + index
		elif num > 9 and num < 100:
			index = '0' + index
		img = base_url + "/" + index + '.jpg'
		img_name = img.split("/")[-1]
		with urllib.request.urlopen(img) as response, open("images" + "/" + img_name, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)
	return True

def main():

    os.mkdir('images')
    base_url = r'[URL]'

    is_download = GetImages(base_url)
    print("Done getting images\n")

if __name__ == '__main__':
    main()
    