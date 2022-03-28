from flask import Flask,render_template,request,redirect,url_for
from pytube import YouTube

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download():
    url = request.args.get('url')
    if url:
        return render_template('download.html')
    else:
        return redirect(url_for('index'))
