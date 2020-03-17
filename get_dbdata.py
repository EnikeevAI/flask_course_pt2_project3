from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from models import User, Meal, Category, Order


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

MEALS_API = 'https://sheetdb.io/api/v1/5lune3fjjyb27'
CATEGORIES_API = 'https://sheetdb.io/api/v1/o3pfar3s5gpui'

meals = requests.get(MEALS_API, params={'q': 'language:python'})
categories = requests.get(CATEGORIES_API, params={'q': 'language:python'})

def add_db_data(categories=categories, meals=meals):
    for category in categories.json():
        category_db = Category(title=category['title'])
        db.session.add(category_db)
        for meal in meals.json():
            if meal['category_id'] == category['id']:
                meal_db = Meal(
                    id = meal['id'],
                    title=meal['title'],
                    price=meal['price'],
                    description=meal['description'],
                    picture=meal['picture'],
                    category=category_db
                    )
                db.session.add(meal_db)
    db.session.commit()

if __name__ == '__main__':
    add_db_data()

        