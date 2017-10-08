import base64
import os
import json

from flask import Flask, redirect, render_template, request
from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision



##takes in the file name

def ML(filename,prevlabel=None):

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get('CLOUD_STORAGE_BUCKET'))
    

    vision_client = vision.ImageAnnotatorClient()
    source_uri = 'gs://{}/{}'.format(os.environ.get('CLOUD_STORAGE_BUCKET'), filename)
    response = vision_client.annotate_image({'image': {'source': {'image_uri': source_uri}},})
    labels = response.label_annotations
    #faces = response.face_annotations
    #web_entities = response.web_detection.web_entities
    
    if labels[0] == prevlabel:
        return labels[1].description
    return labels[0].description