import os
import gtts
from uuid import uuid4
from flask import Flask, request, render_template, send_from_directory
from flask_cors import cross_origin
from subprocess import run
import subprocess
from gtts import gTTS
from playsound import playsound

app = Flask(__name__)
# app = Flask(__name__, static_folder="images")
@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response


def Generator(f):
    alls =[]
    a = subprocess.check_output(["python3", "test.py", "-i", "./static/"+f'{f}']).decode("utf-8")
    l = a.split(' ')
    for i in range(len(l)):
        print(l[i])
        alls.append(l[i])
        alls.append(" ")

    def convert(alls):
        new = "" 
        for x in alls[2:-3]: 
            new += x  
        return new 

    return convert(alls)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", filename=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("image", filename)

@app.route('/complete/<filename>',methods=['POST','GET'])
@cross_origin()
def complete(filename):
    f = request.form['filename']
    result = Generator(f)
    return render_template('result.html',result=result,filename=f)
    """else:
        return render_template('result.html')
    return render_template("result.html",result=result,filename=f)"""

@app.route('/sound/<result>',methods=['POST','GET'])
@cross_origin()
def sound(result):
    mytext = request.form['result']
    language = 'en'
    myobj = gtts.gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    playsound("welcome.mp3")
    return render_template('upload.html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=3333, debug=True)