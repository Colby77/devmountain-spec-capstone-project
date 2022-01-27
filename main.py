"""
main.py
    The main file of the app
    Run this file to start the app
    ('python main.py')
"""
import os
from flask import (Flask, render_template, redirect, flash,
                request, session)

from flask_sqlalchemy import SQLAlchemy

from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.utils import import_string

from database import (User, Product, Auth, Review, Wishlist,
                     )

db = SQLAlchemy()

app = Flask(__name__)


app.jinja_env.undefined = StrictUndefined
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy = SQLAlchemy()
# sqlalchemy.init_app(app)

# Production or development environment
# config = import_string('_config.DevelopmentConfig')() # development configuration
# config = import_string('_config.ProductionConfig')() # production configuration
# config = ''

# if config:

# app.config.from_object(config)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# To test:
# print(dir(config))
# print(config.DATABASE_URI)
# DB_URI = config.DATABASE_URI

def connect_to_db(app):
    '''
    Description:
        Connects flask app to database
    Returns:
        Nothing
    '''
    
    # print(app)
    # print(DB_URI)
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
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

    return render_template('product_page.html', product=product, reviews=reviews)


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
        if user_password.password == password:
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
            new_user = User(
                email=email,
                username=username
            )
            db.session.add(new_user)
            db.session.commit()

            new_user_auth = Auth(
                user_id=new_user.user_id,
                password=password1
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

    api_key = API_KEY

    search= f'https://www.google.com/maps/embed/v1/search?key={api_key}&q=buy+{material}+near+{city}+{state}'

    return render_template('map.html', search=search)


if __name__ == '__main__':

    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    try:
        connect_to_db(app)
    except Exception as err:
        print(f'main error: {err}')
    app.run()
