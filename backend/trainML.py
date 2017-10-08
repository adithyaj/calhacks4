from bingme import *
from goog import ML


def dler2(urllst,query,num):
    count = 0
    rep_count = 0
    while(count < num):
        try:
            print(count)
            urllib.request.urlretrieve(urllst[count], "data/imgsrc/{0}-{1}.png".format(query,count))
            rep_count = 0
            count += 1
        except Exception as e:
            rep_count += 1
            if rep_count > 20:
                del urllst[count]
                num -= 1
                rep_count = 0
            continue



place_file = open("places.txt", "r")
raw_places = place_file.read().split(sep="\n")




data_dict = {}


for place in raw_places[0:10]:
    key_word_dict = {}
    reply=bingMe(place,0)[0]
    imgList = imageURL(reply,num=10)
    print(imgList)

    dler2(imgList,place,len(imgList))
    for i in range(len(imgList)):
        img_name = imageUpload(i,place)
        attb_lst = ML(img_name)
        for attb in attb_lst:
            if attb in key_word_dict.keys():
                key_word_dict[attb] += 1
            else:
                key_word_dict[attb] = 1
    data_dict[place] = key_word_dict

print(data_dict)