from flask import Flask, render_template, redirect, flash
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.utils import import_string

from database import (User, Product, Auth, Review, Wishlist,
                    connect_to_db, db)

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

# Production or development environment
config = import_string('_config.DevelopmentConfig')() # development configuration
# config = import_string('_config.ProductionConfig')() # production configuration

app.config.from_object(config)
# To test:
# print(dir(config))
# print(config.DATABASE_URI)
DB_URI = config.DATABASE_URI



@app.route('/')
def home():
    
    products = Product.query.all()

    return render_template('home.html', products=products)


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

@app.route('/login')
def login_page():

    return render_template('login.html')


@app.route('/register')
def register_page():

    return render_template('register.html')

if __name__ == '__main__':

    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(port=5000)