import json
from inv import *

old_str_list = []
inv_list = open('inv_list_bool.txt', mode='w')
docrange = 60
index = {}
doclist = open('doclist.txt', mode='w')
numofblog = 0
for id in range(1, docrange):

    idname = blogname(id)


    try:
        data = json.load(open(idname))
    except IOError:
        continue
    print(idname)
    doclist.write(str(id) + '\n')
    message = data['text']
    numofblog = id

    tokens = preOp_bool(message)

    for item in tokens:
        inv_location = 0
        try:
            inv_location_pre = index[item]
        except KeyError:
            inv_location_pre = 1
        index[item] = len(old_str_list)
        old_str_list.append(inv_location_pre)
        old_str_list.append(id)


for id in range(1, docrange):

    idname = newsname(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue
    print(idname)
    newsid = id + numofblog
    doclist.write(str(newsid) + '\n')
    message = data['text']

    tokens = preOp_bool(message)

    for item in tokens:
        inv_location = 0
        try:
            inv_location_pre = index[item]
        except KeyError:
            inv_location_pre = 1
        index[item] = len(old_str_list)
        old_str_list.append(inv_location_pre)
        old_str_list.append(newsid)

for i in range(0, len(old_str_list)):
    inv_list.write(str(old_str_list[i]) + '\n')
doclist.write(str(numofblog))
inv_list.close()
doclist.close()
with open("index.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(index))