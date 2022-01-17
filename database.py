from flask_sqlalchemy import SQLAlchemy

from secrets import db_url

db = SQLAlchemy()


class User(db.Model):
    '''db model for users table'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)


class Auth(db.Model):
    '''db model for auth table'''

    __tablename__ = 'auth'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    password = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('auth', order_by=user_id))


class Product(db.Model):
    '''db model for products table'''

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    featured = db.Column(db.Boolean, nullable=True)


class Review(db.Model):
    '''db model for reviews table'''

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    rating = db.Column(db.Integer, nullable=False)
    review_content = db.Column(db.Text(), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', order_by=review_id))
    product = db.relationship('Product', backref=db.backref('reviews', order_by=review_id))


class Wishlist(db.Model):
    '''db model for wishlist table'''

    __tablename__ = 'wishlists'

    wishlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    user = db.relationship('User', backref=db.backref('users', order_by=wishlist_id))
    product = db.relationship('Product', backref=db.backref('products', order_by=wishlist_id))


def connect_to_db(app):
    '''
    Description:
        Connects flask app to database
    Returns:
        Nothing
    '''
    # print(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # print(app)


if __name__ == '__main__':
    from main import app
    # print(app)
    # print(type(app))
    connect_to_db(app)
    print('Database Connected')