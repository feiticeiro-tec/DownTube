from flask import Flask,render_template
from pytube import YouTube

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download(url):
    return render_template('download.html')
