import math


# function: calculate the tf-idf value
def calculate(tf, total_num_n, df):
    tf_idf = (1 + math.log(tf, 10)) * math.log(total_num_n / (df + 1), 10)
    return tf_idf


# function: calculate the cosine value between two vectors
def similarity(vector1, vector2):
    if len(vector1) == 1:
        return vector2[0]
    zero_list = [0] * len(vector1)
    if vector1 == zero_list or vector2 == zero_list:
        return float(1) if vector1 == vector2 else float(0)
    up = 0
    factor1 = 0
    factor2 = 0
    for dimension in range(len(vector1)):
        up += vector1[dimension] * vector2[dimension]
        factor1 += math.pow(vector1[dimension], 2)
        factor2 += math.pow(vector2[dimension], 2)
    cos = up / (math.sqrt(factor1) * math.sqrt(factor2))
    return cos


# transform the num (about ID) into the real name of the blog
def blog_name(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/blogs_' + idstr + '.json'

    return idname


# transform the num (about ID) into the real name of the news
def news_name(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/news_' + idstr + '.json'

    return idname

