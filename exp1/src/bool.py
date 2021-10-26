import json
from inv import *

old_str_list = []
inv_list = open('inv-list_bool.txt', mode='w')

index = {}

for id in range(1, 60000):

    idname = name(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue

    message = data['text']

    tokens = preOp_bool(message)

    for item in tokens:
        inv_location = 0
        try:
            inv_location_pre = index[item]
        except KeyError:
            inv_location_pre = -1
        index[item] = len(old_str_list)
        old_str_list.append(str(inv_location_pre) + '\n')
        old_str_list.append(str(id) + '\n')

inv_list.writelines(old_str_list)

inv_list.close()
