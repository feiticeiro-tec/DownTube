from flask import Flask,render_template,request,redirect,url_for
from pytube import YouTube

app = Flask(__name__)
#__________ FUNCTIONS ___________
def number_to_string(number):
    number = str(number)[::-1]
    number = '.'.join([number[num:num+3]for num in range(0,len(number),3)])
    number = number[::-1]
    if '.' in number:
        number = number[:number.rfind('.')] + ',' + number[number.rfind('.')+1:]
    return number


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download():
    url = request.args.get('url')
    if url:
        video = YouTube(url)
        data = {'titulo':video.title,'thumbnail':video.thumbnail_url,'time':video.length,'data':str(video.publish_date),'views':number_to_string(video.views),'autor':video.author}
        return render_template('download.html',**data)
    else:
        return redirect(url_for('index'))
