import requests
from bs4 import BeautifulSoup

headers = [{'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'},
{'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
]
	
def get_url (filePath):
	searchUrl = 'http://www.google.com/searchbyimage/upload'
	multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
	response = requests.post(searchUrl, files = multipart, allow_redirects = False)
	fetchUrl = response.headers['Location']
	return fetchUrl

j = 0
def get_titles(url, header):
	# print(f"j = {j}")
	real_titles = []
	response = requests.get(url, headers = header, allow_redirects = True)
	soup = BeautifulSoup(response.content, 'html.parser')
	titles = soup.find_all("h3", {"class": "LC20lb DKV0Md"})

	for title in titles:
		real_titles.append(title.text)
	try:
		tag = soup.find_all("a", {"id": "pnnext"})
		print("page: ", 'http://www.google.com' + tag[0]['href'])
		# print(tag[0]['href'])
		real_titles.extend(get_titles('http://www.google.com' + tag[0]['href'], header))

		return real_titles
	except:
		return real_titles

def get_titles_on_web (filePath = "demo.jpg"):
	i = 0
	while True:
		try:
			url = get_url(filePath)
			# print(f"base url {i}: {url}")
			print(f"Try {i}")
			response = requests.get(url, headers = headers[i], allow_redirects = True)
			soup = BeautifulSoup(response.content, 'html.parser')
			title_link_part = soup.find_all("div", {"class": "hdtb-mitem"})
			if title_link_part == []:
				print(f"title_link_part: empty")
			title_page_url = 'http://www.google.com' + title_link_part[0].a['href'] + "&num=1000"
			print(title_page_url)
			titles = get_titles(title_page_url, headers[i])
			# print(len(titles))
			return titles
			
		except:
			i += 1
			if i == 10:
				raise Exception("THERE IS SOMETHING WRONG IS HAPPENING.")