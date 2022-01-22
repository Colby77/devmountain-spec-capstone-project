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


    # create random users
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


    # create specific root user
    root = User(
        user_id=quantity+1,
        email='root@root.com',
        username='root'
    )
    root_auth = Auth(
        auth_id=quantity+1,
        user_id=root.user_id,
        password='root'
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

    # create random fake products
    for x in range(0, quantity):
        title = fake.bs()
        description = fake.text(max_nb_chars=150)
        price = fake.pricetag()

        # Convert pricetag to precise Decimal number
        price = price.replace('$', '')
        price = price.replace(',', '_')
        price = Decimal(price)

        product = Product(
            product_id = x,
            title = title,
            description = description,
            picture_url = '',
            price = price,
            featured = False
        )

        db.session.add(product)

    # create specific products
    mig_welder = Product(
        product_id = x + 1,
        title = 'Easy-Flux Welder',
        description = 'Easy to use mig welder. Green.',
        picture_url = '../static/img/welder-image.jpg',
        price = 199.99,
        featured = True
    )
    tig_gloves = Product(
        product_id = x + 2,
        title = 'Tig-Welding Gloves',
        description = 'Thin leather gloves for tig welding',
        picture_url = '../static/img/tig_gloves.jpg',
        price = 19.99,
        featured = True
    )
    floor_jack = Product(
        product_id = x + 3,
        title = 'Floor Jack',
        description = 'Cool red 3 ton floor jack. Works.',
        picture_url = '../static/img/floor_jack.jpg',
        price = 299.99,
        featured = True
    )
    db.session.add(mig_welder)
    db.session.add(tig_gloves)
    db.session.add(floor_jack)

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
    total = total.count
    count = 0

    for row in db.session.query(Product.product_id).all():
        
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