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
        print(email)
        print(username)
        print(password)
        print('')

        db.session.add(user)
        db.session.add(auth)

    db.session.commit()

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




if __name__ == '__main__':
    connect_to_db(app)

    create_users()
    print('DB Connected')