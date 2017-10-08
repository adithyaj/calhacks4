import scrt
import json
import urllib.request
import urllib.parse
import numpy as np
import webbrowser
import os
import base64

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


"""
bingME
Input: query generated, call # (for json filename)
Output: JSON file (to be the image)


"""
def bingMe(query,callnum,count=35):
    k,v = scrt.getMSFTKey()

    args = urllib.parse.urlencode({'q': query.replace(' ','+'), k: v, 'mkt': 'en-us','count':count,'size':'large','height':500,'width':500,'encodingFormat':'png'})

    #backup
    #submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}&{1}={2}&mkt=en-us'.format(query,k,v)
    
    submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?{0}'.format(args)
    response = urllib.request.urlopen(submission).read().decode('utf-8')

    return response,query,callnum
    #data = json.loads(response)
    
def imageURL(jsonData, num=5):
    urlList = []
    d = json.loads(jsonData);
    numImg = num
    imgList = d["value"]
    if numImg > len(imgList):
        numImg = len(imgList)
    imgSelect = np.random.choice(np.arange(len(imgList)), size=numImg, replace=False)
    for i in imgSelect:
        urlList.append(imgList[i]["contentUrl"])
        #webbrowser.open(imgList[i]["contentUrl"],new=2)

    return urlList

def dler(urllst,query,callnum):
    i = 0
    while(i < len(urllst)):
        try:
            urllib.request.urlretrieve(urllst[i], "data/imgsrc/{0}-{1}.png".format(callnum,query))
            return True
        except Exception as e:
            i+=1
            continue
        break
    urllst = imageURL(query,10)
    return dler(urllst,query,callnum)

def imageUpload(query,callnum):
    """storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get('CLOUD_STORAGE_BUCKET'))

    # Create a new blob and upload the file's content to Cloud Storage.
    blob = bucket.blob("data/imgsrc/{0}-{1}.png".format(callnum,query))
    blob.upload_from_string(
            photo.read(), content_type=photo.content_type)"""

    source_file_name = "data/imgsrc/{0}-{1}.png".format(callnum,query)
    destination_blob_name = "{0}-{1}.png".format(callnum,query)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get('CLOUD_STORAGE_BUCKET'))
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


    # Make the blob publicly viewable.
    blob.make_public()
    image_public_url = blob.public_url
    print('Image {0}: {1} uploaded to {2}.'.format(callnum,
        source_file_name,
        destination_blob_name))

    return destination_blob_name
    #print(json.dumps(data))
    """
    #writing to file, this erases the file if it already existed
    fin = open('data/{0}-{1}.json'.format(callnum,query),'w+')
    fin.close()

    fin = open('data/{0}-{1}.json'.format(callnum,query),'w+')
    fin.write(response)
    end = time.time()
    fin.close()
    """


def paratu(blobname):
    return "https://storage.cloud.google.com/planet-182210/{0}".format(blobname)

def sendVals(lst):
    return lst

def get_answer():
    return 1 ##shivam writes this