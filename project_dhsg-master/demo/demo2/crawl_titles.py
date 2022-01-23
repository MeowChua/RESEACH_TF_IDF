import requests
from bs4 import BeautifulSoup

def get_url (filePath):
	searchUrl = 'http://www.google.com/searchbyimage/upload'
	multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
	response = requests.post(searchUrl, files = multipart, allow_redirects = False)
	fetchUrl = response.headers['Location']
	return fetchUrl

def get_titles(url):
	real_titles = []
	response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}, allow_redirects = True)
	soup = BeautifulSoup(response.content, 'html.parser')
	titles = soup.find_all("h3", {"class": "LC20lb DKV0Md"})

	for title in titles:
		real_titles.append(title.text)
	try:
		tag = soup.find_all("a", {"id": "pnnext"})
		real_titles.extend(get_titles('http://www.google.com' + tag[0]['href']))
		return real_titles
	except:
		return real_titles

def get_titles_on_web (filePath = "demo.jpg"):
	try:
		url = get_url(filePath)
		# print(url)
		response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}, allow_redirects = True)
		soup = BeautifulSoup(response.content, 'html.parser')
		title_link_part = soup.find_all("div", {"class": "hdtb-mitem"})
		title_page_url = 'http://www.google.com' + title_link_part[0].a['href']
		
		titles = get_titles(title_page_url)
		# print(titles)
		return titles
		
	except:
		raise Exception("THERE IS SOMETHING WRONG IS HAPPENING.")