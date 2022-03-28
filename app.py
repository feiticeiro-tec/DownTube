from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download():
    return render_template('download.html')
