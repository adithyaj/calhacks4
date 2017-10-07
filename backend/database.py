import os
import sqlite3
from flask import Flask, request, g, render_template, session, redirect, url_for

class DataBase:

    def __init__(self, application, schema):
        
