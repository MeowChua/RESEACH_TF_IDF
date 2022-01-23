from library.ngrams import predict_main_word
from library.TF_IDF import get_name_of_object_in_image

f = open("temp.txt")
    titles = f.readlines()
f.close()
samples = getTitles(titles)

samples = []

for i in range(1, 10):
    samples.append(random.sample(titles, int(len(titles)*10*i/100)))
samples.append(titles)

def getNgram():
    nameTemp = predict_main_word(titles)
    nameTemp = nameTemp.to_dict()
    nameTemp = list(nameTemp.keys())
    nameNgram = nameTemp[0][0]

    return nameNgram

def getTfIdf():
    f = open("temp.txt")
    titles = f.readlines()
    f.close()
    nameTfIdf = get_name_of_object_in_image(titles)

    return nameTfIdf