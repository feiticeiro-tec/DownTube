from flask import Flask,render_template,request,redirect,url_for,abort,session
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
    elif str(e) == '404 Not Found: Not File':
        return render_template('404.html',message='Arquivo Expirado'),404
    else:
        return render_template('404.html',message='Pagina Não Encontrada!'),404
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def url_download():
    url = request.args.get('url')
    resolution = request.args.get('resolution') #highest or if lower
    format_output = 'mp3' if request.args.get('format')=='mp3' else 'mp4' #highest or if lower
    
    if resolution:
        if resolution == 'highest':
            resolution = True
        else:
            resolution = False
    else:
        resolution = False

    if url:
        try:
            video = YouTube(url)
            if format_output == 'mp3':
                save_in_output(video.streams.filter(only_audio=True).first())
                filename = video.title+'mp3' if video.title[-1] == '.' else video.title+'.mp3'
                if video.title[-1] == '.':
                    os.rename(app.output+video.title+'mp4', app.output+filename)
                else:
                    os.rename(app.output+video.title+'.mp4', app.output+filename)
                    

            elif resolution:
                filename = video.title+'mp4' if video.title[-1] == '.' else video.title+'.mp4'
                save_in_output(video.streams.get_highest_resolution())
            else:
                filename = video.title+'mp4' if video.title[-1] == '.' else video.title+'.mp4'
                save_in_output(video.streams.get_lowest_resolution())
            
            data = {
                'titulo':video.title,
                'thumbnail':video.thumbnail_url,
                'time':secunds_to_string_time(video.length),
                'data':str(video.publish_date),
                'views':number_to_string(video.views),
                'autor':video.author,
                'url_file':url_for('static',filename=f'source/{filename}')}
            return render_template('download.html',**data)
        except RegexMatchError:
            abort(404,description='Not URL')
    else:
        return redirect(url_for('index'))

@app.route('/download/<file_name>')
def download_file(file_name):
    path = f'{os.path.dirname(__file__)}/static/source/{file_name}'
    if os.path.isfile(path):
        return redirect(url_for('static',filename=f'source/{file_name}'))
    else:
        abort(404,description='Not File')
