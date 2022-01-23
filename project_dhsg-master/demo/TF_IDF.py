from collections import Counter
import math
import re

f = open("stop_words.txt") #data.txt
lines = f.readlines()
f.close()

regex = re.compile('[^a-zA-Z]+') 

stop_words = []
for line in lines:
	stop_words.append(line.strip('\n'))

tf_dict = {}
idf_dict = {}
processed_titles = []

def tf (title):
	# max_value = getMaxFrequency(title)
	length = len(title.split())
	elements_count = Counter(title.split())
	for key, value in elements_count.items():
		tf_dict[key] += value/length


def idf (titles, word):
	length = len(titles)
	count = 0

	for title in titles:
		if word in title:
			count += 1

	idf_dict[word] = math.log(length/(count + 1), 10)

def tf_idf(titles):
	tf_idf_dict = {}

	for title in processed_titles:
		tf(title)

	for word in tf_dict.keys():
		idf(processed_titles, word)

	for word in tf_dict.keys():
		tf_idf_dict[word] = tf_dict[word]*idf_dict[word]

	return tf_idf_dict

def preprocess_titles(titles):
	sen = ""
	# print(titles)
	global processed_titles

	for title in titles:
		for word in title.split():
			if len(word) >= 3 and word.lower() not in stop_words and word[-1] not in stop_words and word[0] not in stop_words and regex.search(word) == None:
				sen += word.lower() + " "
		processed_titles.append("".join(sen.rstrip().lstrip()))
		sen = ""


def preprocess_data(titles):
	preprocess_titles(titles)
	global tf_dict
	global idf_dict

	words = []
	for title in processed_titles:
		words = words + title.split()
	uniq_words = set(words)
	tf_dict = dict.fromkeys(uniq_words, 0) 
	idf_dict = dict.fromkeys(uniq_words, 0) 

def get_name_of_object_in_image(titles):
	preprocess_data(titles)
	tf_idf_dict = tf_idf(titles)
	res = max(tf_idf_dict, key=tf_idf_dict.get)
	print(tf_idf_dict)
	global tf_dict
	global idf_dict
	global processed_titles
	tf_dict = {}
	idf_dict = {}
	processed_titles = []
	return res