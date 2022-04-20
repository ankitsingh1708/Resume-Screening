
import glob
import os
import warnings
import textract
import requests
from flask import (Flask,session, g, json, Blueprint,flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from werkzeug import secure_filename
import PyPDF2

import screen
#import search
import hashlib

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
    

@app.route('/')
def home():
   
    return render_template('index.html')


@app.route('/uploadres', methods=['GET', 'POST'])
def uploadres():
    if request.method == 'POST':
        files = glob.glob('./Original_Resumes/*')
        for f in files:
            os.remove(f)

        uploaded_files = request.files.getlist("file[]")
      
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file.save(os.path.join('./Original_Resumes', filename))
        return render_template('index.html')
     
    return render_template('index.html')


@app.route('/uploaddes', methods=['GET', 'POST'])
def uploaddes():
    if request.method == 'POST':
        files = glob.glob('./Job_Description/*')
        for f in files:
            os.remove(f)

        file = request.files['file']
        file.save(os.path.join('./Job_Description', 'Job.txt'))
        return render_template('index.html')
     
    return render_template('index.html')
		

@app.route('/results', methods=['GET', 'POST'])
def res():
        flask_return = screen.res()
        print(flask_return)
        return render_template('result.html', results = flask_return)







@app.route('/Original_Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Original_Resumes', filename)



if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    app.run('localhost' , 8000 , debug=True , threaded=True)
    
