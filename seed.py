from main import app
from database import (connect_to_db, db, User,
                    Auth, Review, Wishlist, Product)

from faker import Faker

fake = Faker()


def create_users():
    '''
    Description:
        Creates fake users and saves them to the
        database
    Returns:
        Nothing
    '''
    User.query.delete()



if __name__ == '__main__':
    connect_to_db(app)

    print('DB Connected')