from flask import Flask, redirect, render_template, request, session, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from forms import CartForm, UserForm
from models import User, Meal, Category, Order


app = Flask(__name__)
app.secret_key = 'Enikeev-project3-secret-phrase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    total_price = session.get('total_price', 0)
    meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
    total_price += meal.price
    cart.append(meal_id)
    session['trash'] = None
    session['cart'] = cart
    session['total_price'] = total_price
    return redirect(url_for('render_cart'))

@app.route('/addtotrash/<meal_id>')
def addtotrash(meal_id):
    cart = session.get('cart')
    total_price = session.get('total_price')
    meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
    cart.remove(meal_id)
    total_price -= meal.price
    session['trash'] = meal.id
    session['cart'] = cart
    session['total_price'] = total_price
    return redirect(url_for('render_cart'))

@app.route('/cart/')
def render_cart():
    meals = []
    if session.get('is_auth'): user_access = True
    else: user_access = False
    trash = session.get('trash', None)
    if trash != None:
        trash_meal = db.session.query(Meal).filter(
                Meal.id == trash).one_or_none()
    else: trash_meal = None
    cart = session.get('cart', [])
    total_price = session.get('total_price', 0)
    user_cart = {'meals_numb': len(cart), 
                'total_price': total_price,
                'trash_meal': trash_meal,
                'user_access': user_access}      
    if len(cart) > 0:
        for meal_id in cart:
            meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
            meals.append(meal)
    cart_form = CartForm()
    #if cart_form.validate_on_submit:
        #return redirect('/ordered')
    return render_template('cart.html', 
                            cart=user_cart,
                            form=cart_form, 
                            meals=meals, 
                            trash=trash)

@app.route('/account/')
def render_account():
    return render_template('account.html')

@app.route('/login/')
def render_login():
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    register_form = UserForm()
    if request.method == 'POST' and register_form.validate_on_submit():
        usermail = request.form.get("userMail")
        password = request.form.get("userPassword")
        new_user = User(mail=usermail,
                        role="Client")
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('render_login'))
    return render_template('register.html', form=register_form)

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