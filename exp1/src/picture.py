import requests
from inv import *
import json

cnt = 0
for id in range(4982, 60000):

    if cnt == 925:
        break
    idname = blogname(id)

    try:
        data = json.load(open(idname))
    except IOError:
        continue

    print(idname)
    savename = picname(id)

    pic_url = data['thread']['main_image']


    url = "https://api.imagga.com/v2/tags"

    querystring = {
        "image_url": pic_url,
        "version": "2"}

    headers = {
        'accept': "application/json",
        'authorization': "Basic YWNjXzBkNWViYjkwOTk1YTc2Zjo2YzBiNDVjMmZkZWVkMGE0ZjQzODgxNzA2NDdlYTk0Ng=="
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open(savename, "w", encoding='utf-8') as f:
        f.write(json.dumps(response.text))

    print(response.text)
