from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

f = open("stop_words.txt") #data.txt
lines = f.readlines()
f.close()

stop_words = []
for line in lines:
	stop_words.append(line.strip('\n'))

processed_titles = []

def preprocess_titles(titles):
	sen = ""
	# print(titles)
	global processed_titles

	for title in titles:
		for word in title.split():
			if len(word) >= 3 and word.lower() not in stop_words and word[-1] not in stop_words:
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

def get_name_of_object_in_image(titles):
	preprocess_data(titles)
	vect = TfidfVectorizer()
	tfidf_matrix = vect.fit_transform(processed_titles)
	df = pd.DataFrame(tfidf_matrix.toarray(), columns = vect.get_feature_names())
	tf_idf_dict = dict.fromkeys(vect.get_feature_names(), 0) 

	for name in vect.get_feature_names():
		# print(name, ":\t", df[name].sum())
		tf_idf_dict[name] = df[name].sum()

	return max(tf_idf_dict, key=tf_idf_dict.get)