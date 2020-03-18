from flask import Flask, redirect, render_template, request, session, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from models import User, Meal, Category, Order


app = Flask(__name__)
app.secret_key = 'Enikeev-project3-secret-phrase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#user_cart = {'meals_numb': 0, 'total_price': 0}
@app.route('/')
def main():
    cart = session.get('cart', [])
    total_price = session.get('total_price', 0)
    user_cart = {'meals_numb': len(cart), 
                'total_price': total_price}
    categories_meals = {}
    categories = db.session.query(Category).all()
    for category in categories:
        categories_meals[category] = []
        meals = db.session.query(Meal).filter(
            Meal.category_id == category.id).order_by(
                func.random()).limit(3)            
        for meal in meals:
            categories_meals[category].append(meal)
    return render_template('main.html', 
                            category_meals=categories_meals,
                            cart = user_cart)

@app.route('/addtocart/<meal_id>')
def addtocart(meal_id):
    cart = session.get('cart', [])
    total_price = 0
    meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
    total_price += meal.price
    cart.append(meal_id)
    session['cart'] = cart
    print(session['cart'])
    if len(cart) > 0:
        for meal_id in cart:
            meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
            total_price += meal.price
            print(total_price)
    session['total_price'] = total_price
    return redirect(url_for('render_cart'))

@app.route('/cart/')
def render_cart():
    meals = []
    cart = session.get('cart', [])
    total_price = session.get('total_price', 0)
    user_cart = {'meals_numb': len(cart), 
                'total_price': total_price}      
    if len(cart) > 0:
        for meal_id in cart:
            meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
            meals.append(meal)
    return render_template('cart.html', cart=user_cart, meals=meals)

@app.route('/account/')
def render_account():
    return render_template('account.html')

@app.route('/login/')
def render_login():
    return render_template('login.html')

@app.route('/register/')
def render_register():
    return render_template('register.html')

@app.route('/logout/')
def render_logout():
    return render_template('auth.html')

@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')        

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()