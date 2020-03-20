from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SubmitField


class CartForm(FlaskForm):
    clientName = StringField('Ваше имя')
    clientAddress = StringField('Адрес')
    clientMail = StringField('Электропочта')
    clientPhone = StringField('Телефон')
    cartSumm = HiddenField('cart_sum')
    cartMeals = HiddenField('cart_meals')
    submit = SubmitField('Оформить заказ')
