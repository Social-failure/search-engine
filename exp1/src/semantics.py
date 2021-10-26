import json
from inv import *
import numpy as np
from scipy.sparse import dok_matrix
import math

old_str_list = []
inv_list = open('inv-list_semantics.txt', mode='w')
index = {}
numofdoc = 0
doclist = {}

for id in range(1, 4000):

    idname = name(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue

    doclist[id] = numofdoc

    numofdoc += 1

    message = data['text']

    tokens = preOp_semantics(message)

    for item in tokens[0]:
        try:
            inv_location_tup = index[item]
        except KeyError:
            inv_location_tup = (-1, 0)
        df = inv_location_tup[1]
        index[item] = (len(old_str_list), df + 1)
        old_str_list.append(str(inv_location_tup[0]) + '\n')
        old_str_list.append(str(id) + '\n')
        old_str_list.append(str(tokens[1][tokens[0].index(item)]) + '\n')

cnt = 0
for i in range(0, len(old_str_list)):
    if cnt != 2:
        inv_list.write(old_str_list[i])
        cnt += 1
    else:
        cnt = 0

S = dok_matrix((len(index), numofdoc), dtype=np.float32)

csr_cnt = 0
for item in index:
    inv_location_tup = index[item]
    inv_location = inv_location_tup[0]
    while inv_location != -1:
        tf = int(old_str_list[inv_location + 2])
        df = inv_location_tup[1]
        val = (1 + math.log(tf, 10)) * math.log((numofdoc / df), 10)
        S[csr_cnt, doclist[int(old_str_list[inv_location + 1])]] = val
        inv_location = int(old_str_list[inv_location])
    csr_cnt += 1

print(S.toarray())
inv_list.close()
