# WeldingStuff.com

## Project Description
A shopping site for welding tools

## MVP
    -Users can see all available products
    -Users can see details about a specific product
    -Users can review/rate products
    -Users can login/logout and register an account
    -User info, reviews and wishlist items are saved to the database
    -All products are saved in the database

#### Bonuses
    -Deployment on heroku
    -Use google maps API to allow users to find welding materials in a given
    city
    -Email notifications

## Data Model
Data model of the database for the project.

#### Info Stored
    -Users: user_id, email, password, username, wishlist items
    -Reviews: review_id, user_id, product_id, review_content, rating
    -Products: product_id, title, description, price, review_id

#### Tables

__users__
- user_id
- username
- email
- wishlist

 __auth__
- 

__reviews__
    -

__products__


#### Relationships

One-Many | Many-Many | One-One
-------- | --------- | -------
One user can have many products on wishlist | Many users review many products through the reviews table | One user to one user_id on auth table
A product has many reviews | |



