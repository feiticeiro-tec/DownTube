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
        try:
            video = YouTube(url)
            if format_output == 'mp3':
                video.streams.filter(only_audio=True).first().download(app.output)
                filename = video.title+'mp3' if video.title[-1] == '.' else video.title+'.mp3'
                if video.title[-1] == '.':
                    os.rename(app.output+video.title+'mp4', app.output+filename)
                else:
                    os.rename(app.output+video.title+'.mp4', app.output+filename)
            else:
                filename = video.title+'mp4' if video.title[-1] == '.' else video.title+'.mp4'
                if resolution:
                    video.streams.get_highest_resolution().download(app.output)
                else:
                    video.streams.get_lowest_resolution().download(app.output)
            
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
        except:
            abort(404,description='Not URL')
    else:
        return redirect(url_for('index'))
