from flask import Flask, render_template, redirect, flash
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.utils import import_string

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

# Production or development environment
config = import_string('_config.DevelopmentConfig')()
# config = import_string('_config.ProductionConfig')()

app.config.from_object(config)
# To test:
# print(dir(config))
# print(config.DATABASE_URI)


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