from collections import Counter
import math

f = open("f1.txt") #data.txt
lines = f.readlines()
f.close()

stop_words = []
for line in lines:
	stop_words.append(line.strip('\n'))

def tf (bag_of_word):
	max_key =  max(bag_of_word, key = bag_of_word.get)
	max_value = bag_of_word[max_key]
	tf_list = []

	for kw in bag_of_word:
		value = (bag_of_word[kw]/(max_value*1.0))
		tf_list.append(value)
	# print(tf_list)

	return tf_list

def idf (titles, word):
	length = len(titles)
	count = 0
	
	for title in titles:
		if word in title:
			count += 1

	# print(word,"  ", count, "  ", math.log(length*1.0/count, 10))
	return math.log(length*1.0/count, 10)

def tf_idf(titles, bag_of_word):
	processed_titles = []
	tf_idf_dict = {}
	tf_idf_list = []
	tf_list = tf(bag_of_word)
	idf_list = []

	for title in titles:
		processed_titles.append(title.lower())

	for word in bag_of_word:
		idf_list.append(idf(processed_titles, word))

	for i in range(len(tf_list)):
		tf_idf_list.append(tf_list[i]*idf_list[i])

	bag_of_word = list(bag_of_word)
	for (word, tf_idf_value) in zip (bag_of_word, tf_idf_list):
		tf_idf_dict[word] = tf_idf_value

	# print (tf_idf_dict)
	return tf_idf_dict

def preprocess_data(titles):
	words = []
	for title in titles:
		words = words + title.split()

	bag_of_word = []
	for word in words:
		word = word.lower()
		if word not in stop_words and word[-1] not in stop_words:
			bag_of_word.append(word)

	bag_of_word = [i for i in bag_of_word if len(i) >= 3]
	bag_of_word = dict(Counter(bag_of_word))

	return bag_of_word

def get_name_of_object_in_image(titles):
	bag_of_word = preprocess_data(titles)

	tf_idf_dict = tf_idf(titles, bag_of_word)
	result_value = tf_idf_dict[min(tf_idf_dict, key = tf_idf_dict.get)]
	
	# print(result_value)
	for key in tf_idf_dict:
		if tf_idf_dict[key] == result_value:
			return key