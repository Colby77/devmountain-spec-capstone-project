from flask_sqlalchemy import SQLAlchemy

import os

# from main import DB_URI

db = SQLAlchemy()


class User(db.Model):
    '''db model for users table'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)

    # user_auth = db.relationship('Auth', back_populates='users', uselist=False)
    user_auth = db.relationship('Auth', backref='users', uselist=False)
    user_review = db.relationship('Review', back_populates='from_user', uselist=False)


class Auth(db.Model):
    '''db model for auth table'''

    __tablename__ = 'auth'

    # auth_id is only because you need a primary key for SQLAlchemy ORM
    auth_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # user = db.relationship('User', backref=db.backref('auth', order_by=user_id))
    # user = db.relationship('User', back_populates='user_auth')


class Product(db.Model):
    '''db model for products table'''

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    picture_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Numeric(), nullable=False)
    featured = db.Column(db.Boolean, nullable=True)

    p = db.relationship('Review', backref='products')

    


class Review(db.Model):
    '''db model for reviews table'''

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    rating = db.Column(db.Integer, nullable=False)
    review_content = db.Column(db.Text(), nullable=False)

    from_user = db.relationship('User', back_populates='user_review')
    # product = db.relationship('Product', backref=db.backref('p', order_by=review_id))


class Wishlist(db.Model):
    '''db model for wishlist table'''

    __tablename__ = 'wishlists'

    wishlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    user = db.relationship('User', backref=db.backref('users', order_by=wishlist_id))
    product = db.relationship('Product', backref=db.backref('products', order_by=wishlist_id))


# def get_current_user_id():
#      '''
#      Description:
#          Gets the value of the current user_id
#          primary key in the 'users' table
#      Parameters:
#          None
#      Returns:
#          Int: the current user_id primary key
#      '''
#      query = "SELECT currval('users_user_id_seq');"
#      result = db.session.execute(query)
#      print(result)



def connect_to_db(app):
    '''
    Description:
        Connects flask app to database
    Returns:
        Nothing
    '''
    from main import DB_URI
    # print(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    from main import app

    # app.config.from_object(config)
    connect_to_db(app)
    # db.create_all()
    print('Database Connected')