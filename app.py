from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import User, Meal, Category, Order


app = Flask(__name__)
app.secret_key = 'Enikeev-project3-secret-phrase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/cart/')
def render_cart():
    return render_template('cart.html')

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