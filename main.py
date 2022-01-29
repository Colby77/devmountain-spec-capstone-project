"""
main.py
    The main file of the app
    Run this file to start the app
    ('python main.py')
Author: Colby Workman
"""
import os
import base64
from io import BytesIO

from flask import (Flask, render_template, redirect, flash,
                request, session)
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import bcrypt

from flask_sqlalchemy import SQLAlchemy

from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.utils import import_string

from database import (User, Product, Auth, Review)

db = SQLAlchemy()

app = Flask(__name__)


app.jinja_env.undefined = StrictUndefined

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.secret_key = os.environ['SECRET_KEY']
    api_key = os.environ['API_KEY']
except KeyError:
    load_dotenv('.env')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.secret_key = os.environ['SECRET_KEY']
    app.config['ENV'] = os.environ['ENV']
    api_key = os.environ['API_KEY']
    environment = os.environ['ENV']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



try:
    db.init_app(app)
except Exception as err:
    print(f'connect_to_db error: {err}')


@app.route('/')
def home():

    query = 'SELECT * FROM products WHERE featured = True;'
    featured_items = db.session.execute(query)

    return render_template('home.html', featured_items=featured_items)


@app.route('/products')
def products_page():

    products = Product.query.all()

    return render_template('products.html', products=products)


@app.route('/products/<int:id>')
def show_product(id):

    product = Product.query.get(id)

    query = """
    SELECT u.username, r.* FROM users u
    INNER JOIN reviews r
    ON r.user_id = u.user_id
    LEFT JOIN products p ON r.product_id = p.product_id
    WHERE p.product_id = {};
    """.format(product.product_id)

    reviews = db.session.execute(query)
    
    with open('record.txt', 'a') as record:
        record.write(f'{product.product_id}| viewed\n')
        record.close()

    return render_template('product_page.html', product=product, reviews=reviews)


@app.route('/views')
def view_count():

    total_views = 0
    product_counts = {}

    views = open('record.txt', 'r')

    for view in views:
        total_views += 1
        view = view.split('|')
        try:
            product_counts[view[0]] += 1
        except KeyError:
            product_counts[view[0]] = 1

    products = list(product_counts.keys())
    counts = list(product_counts.values())

    # Matplotlib Bar Chart
    bar_fig = Figure()

    bar_chart = bar_fig.subplots()
    bar_chart.set_xticks(range(len(counts)), products)
    bar_chart.set_xlabel('Products (product_id)')
    bar_chart.set_ylabel('Views')
    bar_chart.bar(range(len(counts)), counts)

    bar_fig.suptitle('Most Viewed By Count')

    bar_buf = BytesIO()
    bar_fig.savefig(bar_buf, format='png')

    data1 = base64.b64encode(bar_buf.getbuffer()).decode('ascii')

    # Matplotlib Pie Chart
    pie_fig = Figure()

    labels = products
    sizes = counts

    ax1 = pie_fig.subplots()
    ax1.pie(sizes, explode=None, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    # Save it to a temporary buffer.
    buf = BytesIO()
    pie_fig.suptitle('Most Viewed Products by %')
    pie_fig.savefig(buf, format="png")
    data2 = base64.b64encode(buf.getbuffer()).decode("ascii")

    return render_template('view_count.html', data1=data1, data2=data2)


@app.route('/login', methods=['GET'])
def login_page():

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user:
        user_password = Auth.query.filter_by(user_id=user.user_id).first()
        user_password_bytes = bytes(user_password.password, 'utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), user_password_bytes):
            session['user'] = user.username
            print(session)
            flash(f'Welcome {session["user"]}!', 'success')
            return redirect('/')
        else:
            flash('Password incorrect', 'error')
            return redirect('/login')
    else:
        flash('User not found', 'error')
        return redirect('/login')


@app.route('/logout')
def logout():

    session.clear()
    flash('Logged out', 'success')

    return redirect('/')


@app.route('/register', methods=['GET'])
def register_page():

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():

    email = request.form['email']
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']

    user = User.query.filter_by(email=email).first()

    print(email, username, password1, password2)

    if password1 == password2:
        if not user:
            hashed_pw = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            hashed_pw = hashed_pw.decode('utf-8')
            new_user = User(
                email=email,
                username=username
            )
            db.session.add(new_user)
            db.session.commit()

            new_user_auth = Auth(
                user_id=new_user.user_id,
                password=hashed_pw
            )
            db.session.add(new_user_auth)
            db.session.commit()

            flash('Account created', 'success')
            return redirect('/login')
        else:
            flash(f'User with email {email} already exists', 'warning')
            return redirect('/register')
    else:
        flash(f"Passwords don't match", 'warning')
        return redirect('/register')


@app.route('/wishlist')
def show_wishlist():

    product_list = []
    order_total = 0

    if session.get('wishlist'):
        for product, qty in session['wishlist'].items():
            p = Product.query.filter_by(product_id=product).first()
            price = p.price
            p.quantity = qty

            cost = qty * price
            order_total += cost

            print(p)
            product_list.append(p)

    return render_template('wishlist.html', product_list=product_list, order_total=order_total)


@app.route('/add_to_wishlist/<product_id>')
def add_to_wishlist(product_id):

    if session.get('wishlist'):
        if product_id in session['wishlist']:
            session['wishlist'][product_id] += 1
            print(session)
        else:
            session['wishlist'][product_id] = 1
    else:
        session['wishlist'] = {}
        session['wishlist'][product_id] = 1
        print(session)

    flash('Item added to wishlist', 'success')
    return redirect('/wishlist')


@app.route('/checkout')
def checkout():

    flash("Checkout hasn't been implemented", 'info')
    return redirect('/')


@app.route('/map', methods=['GET'])
def show_map():

    return render_template('map.html', search='')

@app.route('/map', methods=['POST'])
def map_search():

    city = request.form['city']
    state = request.form['state']
    material = request.form['material']

    api_key = os.environ['API_KEY']

    search= f'https://www.google.com/maps/embed/v1/search?key={api_key}&q=buy+{material}+near+{city}+{state}'

    return render_template('map.html', search=search)


if __name__ == '__main__':
    app.debug = os.environ['DEBUG']
    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    app.run()
