import re
import unicodedata
import nltk
import pandas as pd 
from nltk.corpus import stopwords

# f = open("./stop_words.txt") #data.txt
# lines = f.readlines()
# f.close()

# stop_words = []
# for line in lines:
#   stop_words.append(line.strip('\n'))

stop_words = set(stopwords.words('english')) 


def basic_clean(text):
	wnl = nltk.stem.WordNetLemmatizer() # đưa các từ về dạng cơ bản. Ví dụ: worked => work
	text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower()) #đưa các từ về lower case
	words = re.sub(r'[^\w\s]', '', text).split() #Bỏ các kí tự đặc biệt
	return [wnl.lemmatize(word) for word in words if word not in stop_words and len(word) >= 3] #trả về các từ không trong stop words, đã được các kí tự đặc biệt và đưa từ về dạng cơ bản

def ngrams(sequence, n):
    history = []
    sequence = iter(sequence)
    
    # while loop được dùng để lấy 2 grams, 3 grams trở lên
    while n > 1:
        try:
            next_item = next(sequence)
        except StopIteration:
            return
        history.append(next_item)
        n -= 1

    for item in sequence:
        history.append(item)
        yield tuple(history) #yield tương tự như return nhưng nó giúp trả về chuỗi kết quả nhanh hơn, nhẹ hơn 
        del history[0] #xoá phần tử đầu thì phần tử thứ 2 là phần tử đầu

def predict_main_word(titles):
	# print("len in ngrams", len(titles))
	text = ""
	for title in titles:
		text += title.replace("\n", "") + " " #đưa tất cả titles vào text
	clean_text = basic_clean(text)#tiền xử lí text qua hàm basic_clean
	return (pd.Series(ngrams(clean_text, 1)).value_counts())[:1] #sử dụng nrams, hàm calue_counts để lấy ra từ có trọng số lớn nhất.