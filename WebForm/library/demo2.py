from ngrams import predict_main_word
# from TF_IDF_lib import get_name_of_object_in_image
from TF_IDF import get_name_of_object_in_image
import time
import random
from tabulate import tabulate
from collections import Counter
import numpy as np

if __name__ == "__main__":
	
	# f = open("../data1.txt") #data.txt
	# f = open("data.txt") #data.txt
	# lines = f.readlines()
	# f.close()

	titles = []
	for line in lines:
		titles.append(line.strip('\n'))

	samples = []

	for i in range(1, 10):
		samples.append(random.sample(titles, int(len(titles)*10*i/100)))
	samples.append(titles)

	results = []
	headers = ["TF-IDF", "Time","N-GRAMS", "Time", "Percentage of data"]
	res = []

	percentage = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

	tfidf_res = []
	ngrams_res = []

	tfidf_time = []
	ngrams_time = []

	predict_main_word(["warm up"]) 
	# vì do ngrams lần đầu chạy phải load WordNetLemmatizer nên lần đầu chạy sẽ lâu hơn thực tế
	# còn các lần thực thi sau mạng đã có trong bộ nhớ đệm 
	# vì vậy các lần thực thi mới có thời gian thực sự khách quan
	# vì thế mới cần dòng 40 

	for i in range (0, 10):	
		# predict_main_word(samples[i])
		#This is tf-idf
		start1 = time.time()
		name1   = get_name_of_object_in_image(samples[i])
		p_time1 = time.time() - start1
		tfidf_res.append(name1)
		tfidf_time.append(p_time1)

		#This is N-gram
		start2 = time.time()
		name2 = predict_main_word(samples[i])
		p_time2 = time.time() - start2
		ngrams_time.append(p_time2)

		name2 = name2.to_dict()
		name2 = list(name2.keys())
		ngrams_res.append(name2[0][0])


		#Add results
		res.append(name1)
		res.append(p_time1)
		res.append(name2[0][0])
		res.append(p_time2)
		res.append((i + 1)*10)
		results.append(res)
		res = []

	print(tabulate(results, headers=headers))

	print(results)
	elements_count_tfidf = Counter(tfidf_res)
	elements_count_ngrams = Counter(tfidf_res)

	most_common_word_tfidf = max(elements_count_tfidf, key=elements_count_tfidf.get)
	most_common_word_ngrams = max(elements_count_ngrams, key=elements_count_ngrams.get)
