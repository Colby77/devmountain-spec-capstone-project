from flask import Flask, render_template, redirect, flash
from jinja2 import StrictUndefined

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined


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

    app.debug = True
    app.run()