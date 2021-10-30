from inv import *
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from scipy.sparse import load_npz
import json
import urllib.request

# get input
message = input("What do you want to search?\n")
inputs = word_tokenize(message)

# delete stopwords in input
clear_input = inputs[:]
for each_input in inputs:
    if each_input in stopwords.words('english'):
        clear_input.remove(each_input)

# get stem of each input and their frequency ( named tf )
stemmer = PorterStemmer()
tokens = []
total_pic = []
total_tag = []
for each_input in clear_input:
    token_stem = stemmer.stem(each_input)
    tokens.append(token_stem)

# get the total num of pictures
with open("../output/picture_list.txt", 'r') as f:
    total_pic = f.readlines()

# get the map of tags
with open("../output/tag_list.txt", 'r') as f:
    total_tag = f.readlines()

# calculate the confidence between query and all picmo
all_con = []
s = load_npz("../output/matrix_pic.npz")
s = s.todok()
for pic_index in range(len(total_pic)):
    pic_confidence = 0
    for tag in range(len(tokens)):
        x_coordinate = total_tag.index(tokens[tag] + '\n')
        pic_confidence += s[x_coordinate, pic_index]
    all_con.append([pic_index, pic_confidence])

all_con.sort(key=lambda x: x[1], reverse=True)

for i in range(10):
    file_id = int(total_pic[all_con[i][0]])
    filename = blogname(file_id)
    print(filename)

for i in range(10):
    result = open('../output/pic_result/' + str(i), mode='wb')
    file_id = int(total_pic[all_con[i][0]])
    filename = blogname(file_id)
    data = json.load(open(filename))
    pic_url = data['thread']['main_image']
    request = urllib.request.urlopen(pic_url)
    buf = request.read()
    result.write(buf)
    result.close()


