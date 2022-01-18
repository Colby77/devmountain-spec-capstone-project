from flask import Flask, render_template, redirect, flash
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = 'secret_key'

app.jinja_env.undefined = StrictUndefined

# Production or development environment
# Set in _config.py file
app.config.from_object('_config.DevConfig')


@app.route('/')
def home():
    
    return render_template('home.html')


@app.route('/login')
def login_page():

    return render_template('login.html')


@app.route('/register')
def register_page():

    return render_template('register.html')

if __name__ == '__main__':

    app.jinja_env.auto_reload = app.debug

    DebugToolbarExtension(app)

    app.run(port=5000)