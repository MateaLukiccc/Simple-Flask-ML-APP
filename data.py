from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

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


if __name__=="__main__":
    app.run(debug=True)
    
