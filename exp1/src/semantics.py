import json
from inv import *

tablesize = 10000

index = [('', -1, 0)] * tablesize

old_str_list = []
inv_list = open('inv-list_semantics.txt', mode='w')

for id in range(1, 40):

    idname = name(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue

    message = data['text']

    tokens = preOp_semantics(message)

    for item in tokens:
        inv_location = 0
        hashloaction = inv_hash(index, item, tablesize)
        inv_location_pre = index[hashloaction][1]
        df = index[hashloaction][2]
        index[hashloaction] = (item, len(old_str_list), df + 1)
        old_str_list.append(str(inv_location_pre) + '\n')
        old_str_list.append(str(tokens[item]) + '\n')
        old_str_list.append(str(id) + '\n')

inv_list.writelines(old_str_list)

inv_list.close()
