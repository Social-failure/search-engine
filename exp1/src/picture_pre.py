from inv import *

for id in range(2, 60000):


    idname = picname(id)
    idnewname = picsname(id)
    try:
        pic = open(idname, mode='r')
    except IOError:
        continue

    newpic = open(idnewname, mode='w')
    str = pic.read()
    newstr = str.replace('\\', '')
    newstr = newstr[1:len(newstr)-1]
    newpic.write(newstr)
    pic.close()
    newpic.close()