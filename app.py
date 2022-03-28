from flask import Flask,render_template,request,redirect,url_for,abort
from pytube import YouTube
from pytube.exceptions import RegexMatchError

app = Flask(__name__)

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
    if url:
        try:
            video = YouTube(url)
            data = {'titulo':video.title,'thumbnail':video.thumbnail_url,'time':secunds_to_string_time(video.length),'data':str(video.publish_date),'views':number_to_string(video.views),'autor':video.author}
            return render_template('download.html',**data)
        except RegexMatchError:
            abort(404,description='Not URL')
    else:
        return redirect(url_for('index'))
