from decimal import Decimal
from random import randint

from main import app
from database import (connect_to_db, db, User,
                    Auth, Review, Wishlist, Product)

from faker import Faker

fake = Faker()


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

    for x in range(0, quantity):
        email = fake.email()
        username = fake.user_name()
        password = fake.password()

        user = User(
            user_id=x,
            email=email,
            username=username
        )

        auth = Auth(
            auth_id=x,
            user_id=user.user_id,
            password=password
        )

        db.session.add(user)
        db.session.add(auth)

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

    for x in range(0, quantity):
        title = fake.bs()
        description = fake.text(max_nb_chars=150)
        price = fake.pricetag()
        featured = fake.boolean()

        # Convert pricetag to precise Decimal number
        price = price.replace('$', '')
        price = price.replace(',', '_')
        price = Decimal(price)

        product = Product(
            product_id = x,
            title = title,
            description = description,
            price = price,
            featured = featured
        )

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
    count = 0

    for row in db.session.query(Product.product_id).all():
        
        rating = randint(1, 5)
        review_content = fake.text(max_nb_chars=150)


        review = Review(
                review_id = count,
                user_id = count,
                product_id = row.product_id,
                rating = rating,
                review_content = review_content
                )
        count += 1

        db.session.add(review)
    
    db.session.commit()
    print('Reviews seeded!')
        

if __name__ == '__main__':
    connect_to_db(app)

    Auth.query.delete()
    Review.query.delete()
    User.query.delete()
    Product.query.delete()

    create_users(20)
    create_products(20)
    create_reviews()

    print('DB Connected')