import json
from basic_operation import *
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from scipy.sparse import load_npz

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
tokens_tf = []
for each_input in clear_input:
    token_stem = stemmer.stem(each_input)
    if token_stem in tokens:
        tokens_tf[tokens.index(token_stem)] += 1
    else:
        tokens_tf.append(1)
        tokens.append(token_stem)

# get the x-coordinate and df of each token in semantic query
with open("../output/index_semantics.json", 'r') as f:
    coordinate_df_dict = json.load(f)


# get the total num of files
with open("../output/doclist_semantics.txt", 'r') as f:
    total_file = f.readlines()
    N = len(total_file) - 1
    blog_news_boundary = int(total_file.pop())

# get the query_vector
query_vector = []
for token_order in range(len(tokens)):
    query_tf_idf = calculate(tokens_tf[token_order], N, coordinate_df_dict[tokens[token_order]][1])
    query_vector.append(query_tf_idf)

# calculate the cos between query_vector and all file_vector
all_cos = []
s = load_npz("../output/matrix_semantics.npz")
s = s.todok()
for file_index in range(N):
    file_vector = []
    for token_order in range(len(tokens)):
        x_coordinate = coordinate_df_dict[tokens[token_order]][0]
        file_vector.append(s[x_coordinate, file_index])
    all_cos.append([file_index, similarity(query_vector, file_vector)])

# sort by the cos value from high to low
all_cos.sort(key=lambda x: x[1], reverse=True)

# output the first 10 file name
for i in range(10):
    file_id = int(total_file[all_cos[i][0]])
    if file_id > blog_news_boundary:
        print(news_name(file_id - blog_news_boundary))
    else:
        print(blog_name(file_id))
