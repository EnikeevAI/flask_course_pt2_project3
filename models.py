from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

orders_meals_association = db.Table('orders_meals',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mail = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)
    address = db.Column(db.String(50))
    role = db.Column(db.String(50), nullable=False)
    orders = db.relationship('Order', back_populates='user_order')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals')
    orders = db.relationship(
        'Order', secondary=orders_meals_association, back_populates='meals')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    meals = db.relationship('Meal', back_populates='category')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_order = db.relationship('User', back_populates='orders')
    meals = db.relationship(
        'Meal', secondary=orders_meals_association, back_populates='orders')


if __name__ == '__main__':
    db.create_all()