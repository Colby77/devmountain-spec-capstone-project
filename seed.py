from decimal import Decimal
from random import randint
import os

from faker import Faker
from sqlalchemy import func
import bcrypt
# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv



from main import app
from database import (db, User, Auth, Review, Product)


# db = SQLAlchemy()
fake = Faker()


def connect_to_db(app):
    '''
    Creates a database context with
    the db connection from main.py
    '''
    db.init_app(app)
    db.app = app
    print('db connected')


def create_users(quantity=10):
    '''
    Description:
        Creates fake users with Faker and saves them to the
        database. Also creates a row in the Auth table with
        the created user's password.
    Parameters:
        quantity: int, amount of products to create
        default: 10
    Returns:
        Nothing
    '''
    Auth.query.delete()
    User.query.delete()


    # create random users
    for x in range(0, quantity):
        email = fake.email()
        username = fake.user_name()
        password = fake.password()

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_pw = hashed_pw.decode('utf-8')

        user = User(
            user_id=x,
            email=email,
            username=username
        )

        auth = Auth(
            auth_id=x,
            user_id=user.user_id,
            password=hashed_pw
        )

        db.session.add(user)
        db.session.add(auth)


    # create specific root user

    hashed_pw = bcrypt.hashpw('root'.encode('utf-8'), bcrypt.gensalt())
    hashed_pw = hashed_pw.decode('utf-8')

    root = User(
        user_id=quantity,
        email='root@root.com',
        username='root'
    )
    root_auth = Auth(
        auth_id=quantity,
        user_id=root.user_id,
        password=hashed_pw
    )

    db.session.add(root)
    db.session.add(root_auth)

    db.session.commit()
    print('Users/Auth seeded!')


def create_products(quantity=10):
    '''
    Description:
        Creates fake product information with Faker and
        saves it to the database
    Parameters:
        quantity: int, amount of fake products to create
        default: 10
    Returns:
        Nothing
    '''
    
    Product.query.delete()

     # create specific products
    mig_welder = Product(
        product_id = 0,
        title = 'Easy-Flux Welder',
        description = 'Easy to use mig welder. Green.',
        picture_url = '../static/img/welder-image.jpg',
        price = 199.99,
        featured = True
    )
    tig_gloves = Product(
        product_id = 1,
        title = 'Tig-Welding Gloves',
        description = 'Thin leather gloves for tig welding',
        picture_url = '../static/img/tig_gloves.jpg',
        price = 19.99,
        featured = True
    )
    floor_jack = Product(
        product_id = 2,
        title = 'Floor Jack',
        description = 'Cool red 3 ton floor jack. Works.',
        picture_url = '../static/img/floor_jack.jpg',
        price = 299.99,
        featured = True
    )
    db.session.add(mig_welder)
    db.session.add(tig_gloves)
    db.session.add(floor_jack)

    count = 3

    # create random fake products
    for x in range(0, quantity):
        # title = fake.bs()
        title = fake.text(max_nb_chars=40)
        description = fake.text(max_nb_chars=150)
        price = fake.pricetag()

        # Convert pricetag to precise Decimal number
        price = price.replace('$', '')
        price = price.replace(',', '_')
        price = Decimal(price)

        product = Product(
            product_id = count,
            title = title,
            description = description,
            picture_url = '',
            price = price,
            featured = False
        )

        count += 1

        db.session.add(product)

    db.session.commit()
    print('Products seeded!')


def create_reviews():
    '''
    Description:
        Creates a fake review for each product in
        the database
    Parameters:
        None
    Returns:
        Nothing
    '''
    Review.query.delete()

    # Create random reviews
    total = db.session.execute('SELECT COUNT(*) FROM users;').first()
    total = total.count - 1
    
    count = 0

    for row in db.session.query(Product.product_id).all():
        
        # make 3 reviews for each product
        for num in range(0, 3):
            random_user = randint(1, total)
            rating = randint(1, 5)
            review_content = fake.text(max_nb_chars=150)

            review = Review(
                    review_id = count,
                    user_id = random_user,
                    product_id = row.product_id,
                    rating = rating,
                    review_content = review_content
                    )
            count += 1

            db.session.add(review)
    
    db.session.commit()
    print('Reviews seeded!')

def set_user_id_seq():
    '''
    Description:
        Resets the user_id sequence to the latest
        user_id primary key
    Parameters:
        None
    Returns:
        Nothing
    '''
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    user_sequence = f"SELECT setval('users_user_id_seq', {max_id});"
    db.session.execute(user_sequence)

    result = db.session.query(func.max(Auth.auth_id)).one()
    max_id = int(result[0])

    auth_sequence = f"SELECT setval('auth_auth_id_seq', {max_id});"
    db.session.execute(auth_sequence)


    db.session.commit()


        

if __name__ == '__main__':

    connect_to_db(app)

    Auth.query.delete()
    Review.query.delete()
    User.query.delete()
    Product.query.delete()

    create_users(20)
    create_products(20)
    create_reviews()

    set_user_id_seq()

    print('DB Connected')