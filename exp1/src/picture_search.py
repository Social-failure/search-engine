from inv import *
import json
from scipy.sparse import dok_matrix, save_npz
import numpy as np

taglist = {}

picturelist = []

doc = open("../output/tag_list.txt", mode='w')
pic = open("../output/picture_list.txt", mode='w')
for id in range(1, 60000):


    idname = picname(id)
    try:
        data = json.load(open(idname))
    except IOError:
        continue
    try:
        tags = data['result']['tags']
    except KeyError:
        continue

    datadict = {}

    pic.write(str(id) + '\n')

    for item in tags:
        tag_name = item['tag']['en']
        tag_confidence = item['confidence']
        try:
            tagindex = taglist[tag_name]
        except KeyError:
            tagindex = len(taglist)
            taglist[tag_name] = tagindex
            doc.write(tag_name + '\n')
        datadict[tag_name] = tag_confidence
    picturelist.append(datadict)

S = dok_matrix((len(taglist), len(picturelist)), dtype=np.float32)

for i in range(len(picturelist)):
    for j in picturelist[i]:
        S[taglist[j], i] = picturelist[i][j]
save_npz("../output/matrix_pic.npz", S.tocoo())


doc.close()
pic.close()