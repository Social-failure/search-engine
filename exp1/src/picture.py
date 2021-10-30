import requests
from inv import *
import json

cnt = 0
for id in range(0, 60000):

    if cnt == 1000:
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

    down = response.text.replace('\\', '')
    down = down[1:len(down) - 1]

    with open(savename, "w", encoding='utf-8') as f:
        f.write(down)

    print(response.text)

    cnt += 1
