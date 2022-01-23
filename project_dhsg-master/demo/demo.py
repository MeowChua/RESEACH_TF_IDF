from ngrams import predict_main_word
from crawl_titles import get_titles_on_web
from TF_IDF import get_name_of_object_in_image
import time
 
if __name__ == "__main__":
	filename= "test.jpg"
	titles  = get_titles_on_web(filename)
	print(len(titles))

	start1 = time.time()
	name1   = get_name_of_object_in_image(titles)
	p_time1 = time.time() - start1

	start2 = time.time()
	name2 = predict_main_word(titles)
	p_time2 = time.time() - start2
	name2 = name2.to_dict()
	name2 = list(name2.keys())
	
	print(name1, ",time: ", p_time1)
	print(name2[0][0], ",time: ", p_time2)