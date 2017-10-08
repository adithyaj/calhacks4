import json
import numpy as np
import webbrowser

def imageURL(fileName="0-City.json", num=1):
    urlList = []
    with open(fileName) as jsonData:
        d = json.load(jsonData);
        numImg = num
        imgList = d["value"]
        if numImg > len(imgList):
            numImg = len(imgList)
        imgSelect = np.random.choice(np.arange(len(imgList)), size=numImg, replace=False)
        for i in imgSelect:
            urlList.append(imgList[i]["contentUrl"])
            webbrowser.open(imgList[i]["contentUrl"],new=2)

    return urlList