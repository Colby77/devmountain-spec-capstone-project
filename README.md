# DIYers.com

## Project Description
A shopping site for do-it-yourself-ers

Deployed on heroku: https://devmountain-spec-project-cw.herokuapp.com/

A shopping site for do-it-yourself-ers.  The site would sell tools for peoples' hobbies like welding or woodworking or automotive related stuff.  The features include basic website functionality like registering an account and adding items to the 'cart'.  I also added a supply locator feature where users can enter a city and material they need and find stores where to buy the material near the city.  Every time a product is viewed, it is counted and represented in a graph as well.

The biggest challenges in this project were using SQLAlchemy to model the database tables and deploying the site on heroku.  While I used bootstrap to save a massive amount of time styling and create a nice look, it was tricky to learn how to use as well.

## Tech Used
    -Python
        -Flask
        -SQLAlchemy
        -Matplotlib
    -Bootstrap
    -HTML/CSS
    -PostgreSQL
    -Google Maps Embed API: https://developers.google.com/maps/documentation/embed/get-started

## Data Model
Data model of the database for the project.

<img src='welding_site_db_model.png' height=500px>

#### Info Stored
    -Users: user_id, email, password, username
    -Reviews: review_id, user_id, product_id, review_content, rating
    -Products: product_id, title, description, price

#### Tables

__users__
- *user_id*, serial primary key
- _username_, varchar(255) unique not null
- _email_, varchar(255) unique not null

__auth__
- *user_id*, references users
- username/password are stored and checked here for login

__reviews__
- *review_id*, serial primary key
- *user_id*, references users
- *product_id*, references products
_ *rating*, integer out of 5
_ *review_content*, text review of product

__products__
- *product_id*, serial primary key
- *title*, varchar(255)
- *description*, text description
- *price*, float
- *featured*, boolean true if the product is featured


#### Relationships

One-Many | Many-Many | One-One
-------- | --------- | -------
A product has many reviews | Many users review many products through the reviews table | One user to one user_id on auth table
 | |



