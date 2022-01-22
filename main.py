from flask import (Flask, render_template, redirect, flash,
                request, session)
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
    user_password = Auth.query.filter_by(user_id=user.user_id).first()

    if user:
        if user_password.password == password:
            session['user'] = user.username
            print(session)
            flash(f'Welcome {user.username}!', 'success')
            return redirect('/')
        else:
            flash('Password incorrect', 'error')
            return redirect('/login')
    else:
        flash('User not found', 'error')
        return redirect('/login')


@app.route('/logout')
def logout():

    del session['user']
    flash('Logged out', 'success')
    print(session)
    return redirect('/')


@app.route('/register')
def register_page():

    return render_template('register.html')

if __name__ == '__main__':

    app.jinja_env.auto_reload = app.debug
    DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(port=5000)