import json
import numpy as np
import webbrowser

def imageURL(fileName, num=1):
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
            #webbrowser.open(imgList[i]["contentUrl"],new=2)

    return urlList


def imageUpload():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get('CLOUD_STORAGE_BUCKET'))

    # Create a new blob and upload the file's content to Cloud Storage.
    photo = request.files['file']
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(
            photo.read(), content_type=photo.content_type)

    # Make the blob publicly viewable.
    blob.make_public()
    image_public_url = blob.public_url