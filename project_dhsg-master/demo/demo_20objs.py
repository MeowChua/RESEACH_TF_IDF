from ngrams import predict_main_word
from crawl_titles import get_titles_on_web
from TF_IDF import get_name_of_object_in_image
import time
import os
from tabulate import tabulate


if __name__ == "__main__":
	result_sets = [] 
	
	
	for filename in os.listdir("test_img"):
		result_set = []
		print(filename)
		titles  = get_titles_on_web("test_img/" + filename)
		print(len(titles))
		if titles == 0:
			pass

		start1 = time.time()
		name1   = get_name_of_object_in_image(titles)

		p_time1 = time.time() - start1

		start2 = time.time()
		name2 = predict_main_word(titles)
		p_time2 = time.time() - start2

		name2 = name2.to_dict()
		name2 = list(name2.keys())

		result_set.append(filename)
		result_set.append(name2[0][0])
		result_set.append(p_time2)
		result_set.append(name1)
		result_set.append(p_time1)

		result_sets.append(result_set)
		print(name1, ",time: ", p_time1)
		print(name2[0][0], ",time: ", p_time2, "\n\n")
		# time.sleep(5)
		

print(tabulate(result_sets, headers=["Image", "Ngrams", "Time", "TF IDF", "Time"]))