from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def str_hex_mod(Str, tablesize):
    r = 0
    for c in Str:
        if c <= '9':
            r += r * 16 + int(c)
        else:
            r += r * 16 + ord(c) - 87
        r %= tablesize
    return r




def inv_hash(hashtable, item, tablesize):
    location = hash(item) % (tablesize - 1)
    while hashtable[location] != ('', -1) and hashtable[location][0] != item:
        location = hash(location + 0.1) % (tablesize - 1)
    return location


def name(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '2018_01/blogs_' + idstr + '.json'

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
    finallist = {'':  1}

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)

    tokens = []

    for token in clean_tokens:
        tokens.append(stemmer.stem(token))

    for token in tokens:
        if token not in finallist:
            finallist[token] = 1
        else:
            finallist[token] += 1

    return finallist

