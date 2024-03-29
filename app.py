from flask import (
    render_template,
    redirect,
    request,
    url_for,
    session,
    Flask,
    abort
    )
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import os
from random import choice

app = Flask(__name__)
app.secret_key='secret'
app.output = f'{os.path.dirname(__file__)}/static/source/'

#__________ FUNCTIONS ___________
def number_to_string(number):
    number = str(number)[::-1]
    number = '.'.join([number[num:num+3]for num in range(0,len(number),3)])
    number = number[::-1]
    if '.' in number:
        number = number[:number.rfind('.')] + ',' + number[number.rfind('.')+1:]
    return number

def secunds_to_string_time(number):
    return f'{number//60}:{number%60}'

def save_in_output(file):
    file.download(app.output)

def download(url,resolution,format_output):
    try:
        video = YouTube(url)
        filename = video.title.replace('.','')
        filename = filename+format_output if filename[-1] == '.' else f'{filename}.{format_output}'

        if format_output == 'mp3':
            video.streams.filter(only_audio=True).first().download(app.output)
            if video.title[-1] == '.':
                os.rename(app.output+video.title.replace('.','')+'mp4', app.output+filename)
            else:
                os.rename(app.output+video.title.replace('.','')+'.mp4', app.output+filename)
        else:
            if resolution:
                video.streams.get_highest_resolution().download(app.output)
            else:
                video.streams.get_lowest_resolution().download(app.output)
        return filename,video
    except:
        return None,None

#__________ ROUTES ___________

@app.errorhandler(404)
def page_not_found(e):
    if str(e) == '404 Not Found: Not URL':
        return render_template('404.html',message='Url Não Encontrada!'),404
    else:
        return render_template('404.html',message='Pagina Não Encontrada!'),404
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download():
    url = request.args.get('url')
    resolution = request.args.get('resolution') #highest or if lower
    format_output = 'mp3' if request.args.get('format')=='mp3' else 'mp4' 
    
    if resolution and resolution == 'highest':
        resolution = True
    else:
        resolution = False

    if url:
        filename,video = download(url,resolution,format_output)
        if filename:
            data = {
                'titulo':video.title,
                'thumbnail':video.thumbnail_url,
                'time':secunds_to_string_time(video.length),
                'data':str(video.publish_date),
                'views':number_to_string(video.views),
                'autor':video.author,
                'url_file':url_for('static',filename=f'source/{filename}')
                }
            return render_template('download.html',**data)
        else:
            abort(404,description='Not URL')
    else:
        return redirect(url_for('index'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')