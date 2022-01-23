from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
from collections import Counter
import math
import re
import nltk
from nltk.stem import WordNetLemmatizer
import unicodedata
from nltk.corpus import stopwords

# f = open("./stop_words.txt") #data.txt
# lines = f.readlines()
# f.close()

# stop_words = []
# for line in lines:
# 	stop_words.append(line.strip('\n'))

stop_words = set(stopwords.words('english')) 

processed_titles = []

def preprocess_titles(titles):
	sen = ""
	global processed_titles
	wnl = WordNetLemmatizer()

	for title in titles:
		title = (unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower()) #đưa các từ về lower case
		words = re.sub(r'[^\w\s]', '', title).split()
		for word in words:
			word = wnl.lemmatize(word.lower()) 
			if len(word) >= 3 and word.lower() not in stop_words and re.search('[^a-zA-Z]+', word) == None and re.search("[a-z]+ed", word) == None and re.search("[a-z]+est", word) == None and re.search("[a-z]+ing", word) == None and re.search("[a-z]+tion", word) == None and re.search("[a-z]+ty", word) == None and re.search("[a-z]+ish", word) == None:
				sen += word.lower() + " "
		processed_titles.append("".join(sen.rstrip().lstrip()))
		sen = ""


def preprocess_data(titles):
	preprocess_titles(titles)

	words = []
	for title in processed_titles:
		words = words + title.split()

def get_name_of_object_in_image(titles):
	# print("len in tfidf", len(titles))
	global processed_titles
	preprocess_data(titles)
	vect = TfidfVectorizer()
	tfidf_matrix = vect.fit_transform(processed_titles)
	df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names())
	tf_idf_dict = dict.fromkeys(vect.get_feature_names(), 0) 

	for name in vect.get_feature_names():
		tf_idf_dict[name] = df[name].sum()

	processed_titles = []

	return max(tf_idf_dict, key=tf_idf_dict.get)