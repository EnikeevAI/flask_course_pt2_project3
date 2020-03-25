import datetime
from flask import Flask, redirect, render_template, request, session, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from forms import CartForm, LoginForm, RegisterForm
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
                            cart = user_cart,
                            user_access=session.get('is_auth'))

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

@app.route('/cart/',  methods=['GET', 'POST'])
def render_cart():
    cart_form = CartForm()
    meals = []
    trash = session.get('trash', None)
    if trash != None:
        trash_meal = db.session.query(Meal).filter(
                Meal.id == trash).one_or_none()
    else: trash_meal = None
    cart = session.get('cart', [])
    total_price = session.get('total_price', 0)
    user_cart = {'meals_numb': len(cart), 
                'total_price': total_price,
                'trash_meal': trash_meal}      
    if len(cart) > 0:
        for meal_id in cart:
            meal = db.session.query(Meal).filter(
                Meal.id == meal_id).one_or_none()
            meals.append(meal)
    
    if request.method == 'POST' and cart_form.validate_on_submit():
        today = datetime.datetime.today()

        client_order = {
            "clientName": cart_form.clientName.data,
            "clientAddress": cart_form.clientAddress.data,
            "clientMail": cart_form.clientMail.data,
            "clientPhone": cart_form.clientPhone.data,
            "cartSumm": cart_form.cartSumm.data,
            "cartMeals": cart_form.cartMeals.data 
        }
        client = User.query.filter_by(id=session['user']['id']).one_or_none()
        if client and int(client_order['cartSumm']) > 0:
            order_db = Order(
                date = today.strftime("%Y-%m-%d-%H:%M"),
                sum = total_price,
                status = 'Ready', 
                user_id = client.id)
            for meal in meals:
                order_db.meals.append(meal)
            db.session.add(order_db)
            db.session.commit()
            session['trash'] = []
            session['cart'] = []
            session['total_price'] = 0
            return redirect(url_for('render_ordered'))
        elif client_order['cartSumm'] == 0:
            cart_form.clientPhone.errors.append("Добавьте товары в корзину для оформления заказа")
        else: cart_form.clientMail.errors.append("Неверный адрес электронной почты")
    return render_template('cart.html', 
                            cart=user_cart,
                            form=cart_form, 
                            meals=meals, 
                            trash=trash,
                            user_access=session.get('is_auth'))

@app.route('/account/')
def render_account():
    cart = session.get('cart', [])
    total_price = session.get('total_price')
    user_cart = {'meals_numb': len(cart), 
                'total_price': total_price}
    months = {'01': 'Января',
            '02': 'Февраля',
            '03': 'Марта',
            '04': 'Апреля',
            '05': 'Мая',
            '06': 'Июня',
            '07': 'Июля',
            '08': 'Августа',
            '09': 'Сентября',
            '10': 'Октября',
            '11': 'Ноября',
            '12': 'Декабря'}
    user_orders = {}
    order_price = {}
    orders = Order.query.filter_by(user_id=session['user']['id']).all()
    for order in orders:
        date = []
        for time in order.date.split('-'): date.append(time)
        date[1] = months[date[1]]
        date = " ".join(date[::-1])
        user_orders[date] = []
        order_price[date] = 0
        for meal in order.meals:
            meal_dict = {meal.title: meal.price}
            order_price[date] += int(meal.price)
            user_orders[date].append(meal_dict)
    return render_template('account.html', 
                            cart=user_cart, 
                            orders=user_orders,
                            total_price=order_price,
                            user_access=session.get('is_auth'))

@app.route('/login/', methods=['GET', 'POST'])
def render_login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        usermail = request.form.get("userMail")
        password = request.form.get("userPassword")
        user = User.query.filter_by(mail=usermail).first()
        if user and user.password_valid(password):
            session["user"] = {
                "id": user.id,
                "usermail": user.mail,
                "role": user.role
            }
            session['is_auth'] = True
            return redirect(url_for('main'))
        else: login_form.userMail.errors.append("Неверный адрес электропочты или пароль")
    return render_template('login.html', form=login_form)

@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    register_form = RegisterForm()
    error_msg = None
    if request.method == 'POST' and register_form.validate_on_submit():
        username = request.form.get("userName")
        usermail = request.form.get("userMail")
        password = request.form.get("userPassword")
        useraddress = request.form.get("userAddress")
        user = User.query.filter_by(mail=usermail).first()
        if user:
            error_msg = "Пользователь с укащанной электропочтой уже зарегистрирован"
            return render_template('register.html', 
                                form=register_form, 
                                error_msg=error_msg)
        new_user = User(
                    name=username,
                    mail=usermail,
                    address=useraddress,
                    role="Client")
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('render_login'))
    return render_template('register.html', form=register_form, error_msg=error_msg)

@app.route('/logout/')
def render_logout():
    session.clear()
    return redirect(url_for('render_login'))

@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')        

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()