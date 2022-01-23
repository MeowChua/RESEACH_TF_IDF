import os
import sys
import time
import requests  
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

def get_html_source_by_selenium(url):
    driver_chrome = webdriver.Chrome("chromedriver.exe")
    driver_chrome.get(url)
    driver_chrome.refresh()
    return driver_chrome.page_source


def get_url (filePath):
	searchUrl = 'http://www.google.com/searchbyimage/upload'
	multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
	response = requests.post(searchUrl, files = multipart, allow_redirects = False)
	fetchUrl = response.headers['Location'] 
	return fetchUrl

def get_img_page_html_source_by_selenium(url):
	driver_chrome = webdriver.Chrome('chromedriver.exe')
	driver_chrome.get(url)

	i = 0

	while i < 10:
		driver_chrome.execute_script("window.scrollBy(0,document.body.scrollHeight)")
		try:
			driver_chrome.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
		except Exception:
			pass
		time.sleep(3)
		i += 1

	return driver_chrome.page_source

def download_image(folder_name):
	url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=' + folder_name.replace(' ', '+')
	page = get_img_page_html_source_by_selenium(url)
	soup = BeautifulSoup(page, 'html.parser')

	img_tags = soup.find_all("img", class_="rg_i")

	imagelinks = []
	for img_tag in img_tags:
		try:
			imagelinks.append(img_tag['src'])
		except:
			imagelinks.append(img_tag['data-src'])
	print(f"Found {len(imagelinks)} images")

	try:
		os.mkdir('D:/project/demo/{}'.format(folder_name))
		path = './' + folder_name + '/'
		count = 0
		for imagelink in imagelinks:
		    try:
		        urllib.request.urlretrieve(imagelink, path + str(count) + ".jpg")
		        count += 1
		        print("Image no." + str(count) + " downloaded successfully",end='\r')
		    except Exception:
		        pass
		    if count == 1000:
		      break
	except Exception:
		print("This object's images have already been collected.")
	print("Done.")