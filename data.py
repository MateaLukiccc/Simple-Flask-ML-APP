from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/home/lukic/Desktop/FaceDetection/Simple-Flask-ML-APP/uploaded'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename:str)->bool:
    print(filename.split('.')[-1].lower())
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index/')
def redirect_to_index():
    return redirect(url_for('index'))

@app.route('/user/<name>')
@app.route('/user/')
def user(name=None):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notFound.html'), 404
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       # check if the post request has the file part
       if 'file' not in request.files:
           print("NO FILE")
           return redirect(request.url)
       f = request.files['file']
       if f.filename == '':
           print("NO FILE NAME")
           return redirect(request.url)
       if f and allowed_file(f.filename):
           filename = secure_filename(f.filename)
           print("ALL GOOD")
           f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return redirect(url_for('uploaded_file', filename=filename))
       else:
           print("NOT UPLOADED")
   return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)
    
