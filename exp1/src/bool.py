import json
from inv import *

str_list = []
inv_list = open('../output/inv_list_bool.txt', mode='w')
docrange = 60
index = {}
doclist = open('../output/doclist.txt', mode='w')
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
            inv_location_pre = index[item][0]
            inv_id_pre = index[item][1]
        except KeyError:
            inv_location_pre = 1
            inv_id_pre = id
        index[item] = (len(str_list), id)
        str_list.append(len(str_list) - inv_location_pre)
        str_list.append(id - inv_id_pre)


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
            inv_location_pre = index[item][0]
            inv_id_pre = index[item][1]
        except KeyError:
            inv_location_pre = 1
            inv_id_pre = newsid
        index[item] = (len(str_list), newsid)
        str_list.append(len(str_list) - inv_location_pre)
        str_list.append(newsid - inv_id_pre)

for i in range(0, len(str_list)):
    inv_list.write(str(str_list[i]) + '\n')
doclist.write(str(numofblog))
inv_list.close()
doclist.close()
with open("../output/index.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(index))
