from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def blogname(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/blogs_' + idstr + '.json'
    return idname

def newsname(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/news_' + idstr + '.json'
    return idname

def picname(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/picture_' + idstr + '.json'
    return idname

def picsname(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/pictures_' + idstr + '.json'
    return idname


def preOp_bool(message):

    stopwords.words('english')
    stemmer = PorterStemmer()

    tokens = word_tokenize(message)
    clean_tokens = tokens[:]
    finallist = []

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)

    tokens = []

    for token in clean_tokens:
        tokens.append(stemmer.stem(token))

    for token in tokens:
        if token not in finallist:
            finallist.append(token)

    return finallist


def preOp_semantics(message):

    stopwords.words('english')
    stemmer = PorterStemmer()

    tokens = word_tokenize(message)
    clean_tokens = tokens[:]
    finallist = []
    countlist =[]

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)

    tokens = []

    for token in clean_tokens:
        tokens.append(stemmer.stem(token))

    for token in tokens:
        if token not in finallist:
            finallist.append(token)
            countlist.append(1)
        else:
            countlist[finallist.index(token)] += 1

    finaltup = (finallist, countlist)

    return finaltup

