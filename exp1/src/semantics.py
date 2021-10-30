import json
from inv import *
import numpy as np
import math
from scipy.sparse import dok_matrix, save_npz

data_list = []
index = {}
numofdoc = 0
doclist = {}
docrange = 60000
numofblog = 0

doc = open("../output/doclist_semantics.txt", mode='w')

for id in range(1, docrange):

    idname = blogname(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue

    print(idname)

    numofblog = id
    doc.write(str(id) + '\n')
    doclist[id] = numofdoc

    numofdoc += 1

    message = data['text']

    tokens = preOp_semantics(message)

    for item in tokens[0]:
        try:
            inv_location_tup = index[item]
        except KeyError:
            inv_location_tup = (1, 0)
        df = inv_location_tup[1]
        index[item] = (len(data_list), df + 1)
        data_list.append(inv_location_tup[0])
        data_list.append(id)
        data_list.append(tokens[1][tokens[0].index(item)])

for id in range(1, docrange):

    idname = newsname(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue
    print(idname)
    newsid = id + numofblog
    doc.write(str(newsid) + '\n')
    doclist[newsid] = numofdoc

    numofdoc += 1

    message = data['text']

    tokens = preOp_semantics(message)

    for item in tokens[0]:
        try:
            inv_location_tup = index[item]
        except KeyError:
            inv_location_tup = (1, 0)
        df = inv_location_tup[1]
        index[item] = (len(data_list), df + 1)
        data_list.append(inv_location_tup[0])
        data_list.append(newsid)
        data_list.append(tokens[1][tokens[0].index(item)])

S = dok_matrix((len(index), numofdoc), dtype=np.float32)
index_map = {}
csr_cnt = 0
for item in index:

    inv_location_tup = index[item]
    inv_location = inv_location_tup[0]
    df = inv_location_tup[1]
    index_map[item] = (csr_cnt, df)
    while inv_location != 1:
        tf = data_list[inv_location + 2]
        val = (1 + math.log(tf, 10)) * math.log((numofdoc / df), 10)
        S[csr_cnt, doclist[data_list[inv_location + 1]]] = val
        inv_location = int(data_list[inv_location])
    csr_cnt += 1


with open("../output/index_semantics.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(index_map))

save_npz("../output/matrix_semantics.npz", S.tocoo())

doc.write(str(numofblog))
doc.close()
