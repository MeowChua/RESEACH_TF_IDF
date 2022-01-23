from flask import Flask, render_template, url_for, request
import os
import random
import time
from collections import Counter
from library.crawl_titles import get_titles_on_web
from library.ngrams import predict_main_word
from library.TF_IDF_lib import get_name_of_object_in_image
from library.download_image import download_image
from library.camera import get_image_by_webcam

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    filename = None    
    nameNgram = None
    nameTfIdf = None
    titles = []
    samples = []
    resTimeTfIdf = []
    resTimeNgram = []
    resNgram = []
    resTfIdf = []
    resNgramLength = int(0)
    resTfIdfLength = int(0)

    # print("first titles: ", titles)
    flag = 0
    if request.method == 'POST':
        print("get")
        # print(request.form.get("check"))
        print(request.form.get("check"))
        if request.form.get("check") == "cAm":
            flag = 1
            filename = get_image_by_webcam("demo.jpg")
            titles = get_titles_on_web(filename)

            for i in range(1,4):            
                samples.append(random.sample(titles, int(len(titles)*25*i/100)))
            samples.append(titles)
            for i in range(0,4):
                #This is N-gram section
                if i == 0:
                    predict_main_word(samples[i])## THIS IS WARM UP

                startNgram = time.time()
                nameTemp = predict_main_word(samples[i])
                nameTemp = nameTemp.to_dict()
                nameTemp = list(nameTemp.keys())
                nameNgram = nameTemp[0][0]
                
                timeNgram = time.time() - startNgram
                

                #This is TF-IDF section
                startTfIdf = time.time()
                nameTfIdf = get_name_of_object_in_image(samples[i])
                
                timeTfIdf = time.time() - startTfIdf

                #Add to result array
                resNgram.append(nameNgram)
                resTfIdf.append(nameTfIdf)

                # print("nameTfIdf: ",nameTfIdf)

                rtimeNgram = round(timeNgram,5)
                rtimeTfIdf = round(timeTfIdf,5)

                resTimeNgram.append(rtimeNgram)
                resTimeTfIdf.append(rtimeTfIdf)

            resNgramLength = len(resNgram)
            resTfIdfLength = len(resTfIdf)

    
    if request.method == 'POST' and flag == 0:
        file = request.files['file']
        filename = file.filename
        print

        if bool(filename) == True:
            if (filename.split("."))[-1] != 'txt':
                print(os.path.join("static\\images", filename))
                file.save(os.path.join("static\\images", filename))
                filename = os.path.join("static\\images", filename)
                titles = get_titles_on_web(filename)
            else:
                print(os.path.join("static\\titles", filename))
                file.save(os.path.join("static\\titles", filename))
                filename = os.path.join("static\\titles", filename)

                f = open(filename) #data.txt
                lines = f.readlines()
                f.close()

                titles = []
                for line in lines:
                    titles.append(line.strip('\n'))

                 
            for i in range(1,4):            
                samples.append(random.sample(titles, int(len(titles)*25*i/100)))
            samples.append(titles)
            for i in range(0,4):
                #This is N-gram section
                if i == 0:
                    predict_main_word(samples[i])## THIS IS WARM UP

                startNgram = time.time()
                nameTemp = predict_main_word(samples[i])
                nameTemp = nameTemp.to_dict()
                nameTemp = list(nameTemp.keys())
                nameNgram = nameTemp[0][0]
                
                timeNgram = time.time() - startNgram
                

                #This is TF-IDF section
                startTfIdf = time.time()
                nameTfIdf = get_name_of_object_in_image(samples[i])
                
                timeTfIdf = time.time() - startTfIdf

                #Add to result array
                resNgram.append(nameNgram)
                resTfIdf.append(nameTfIdf)

                # print("nameTfIdf: ",nameTfIdf)

                rtimeNgram = round(timeNgram,5)
                rtimeTfIdf = round(timeTfIdf,5)

                resTimeNgram.append(rtimeNgram)
                resTimeTfIdf.append(rtimeTfIdf)

            resNgramLength = len(resNgram)
            resTfIdfLength = len(resTfIdf)
        else:
            flag = 0
    return render_template('index.html', filename=filename, lenNgram = resNgramLength, lenTfIdf = resTfIdfLength ,ngramName = resNgram, tfidfName = resTfIdf, resTimeNgramx = resTimeNgram, resTimeTfIdfx = resTimeTfIdf)

if __name__ == "__main__":
    app.run(debug=True)
