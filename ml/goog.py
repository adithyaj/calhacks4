import base64
import os

from flask import Flask, redirect, render_template, request
from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


def ML(picname) 