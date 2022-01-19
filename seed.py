from decimal import Decimal

from main import app
from database import (connect_to_db, db, User,
                    Auth, Review, Wishlist, Product)

from faker import Faker

fake = Faker()


def create_users():
    '''
    Description:
        Creates fake users with Faker and saves them to the
        database. Also creates a row in the Auth table with
        the created user's password.
    Parameters:
        None
    Returns:
        Nothing
    '''
    Auth.query.delete()
    User.query.delete()

    for x in range(0, 2):
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

def create_products():
    '''
    Description:
        Creates fake product information with Faker and
        saves it to the database
    Parameters:
        None
    Returns:
        Nothing
    '''
    
    Product.query.delete()

    for x in range(0, 2):
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


if __name__ == '__main__':
    connect_to_db(app)

    create_users()
    create_products()

    print('DB Connected')