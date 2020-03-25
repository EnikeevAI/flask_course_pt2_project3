from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


class CartForm(FlaskForm):
    clientName = StringField('Ваше имя',
                             validators=[InputRequired(message="Введите своё имя")])
    clientAddress = StringField('Адрес',
                                validators=[InputRequired(message="Введите адрес доставки")])
    clientMail = StringField('Электропочта',
                             validators=[Email(message="Некорректный формат адреса электропочты")])
    clientPhone = StringField('Телефон',
                              validators=[InputRequired(message="Введите свой номер телефона"),
                                          Length(min=10, message="Слишком короткий номер")])
    cartSumm = HiddenField('cart_sum')
    cartMeals = HiddenField('cart_meals')
    submit = SubmitField('Оформить заказ')


class RegisterForm(FlaskForm):
    userName = StringField('Ваше имя',
                           validators=[InputRequired(message="Введите своё имя")])
    userMail = StringField('Электропочта',
                           validators=[Email(message="Некорректный формат адреса электропочты"),
                                       InputRequired(message="Введите свою электропочту")])
    userPassword = StringField(
        'Пароль', validators=[InputRequired(message="Введите свой пароль"),
                              Length(min=5, message="Пароль не должен быть короче 5 символов")])
    userAddress = StringField('Ваш Адрес',
                              validators=[InputRequired(message="Введите адрес доставки")])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    userMail = StringField('Электропочта',
                           validators=[Email(message="Некорректный формат адреса электропочты"),
                                       InputRequired(message="Введите свою электропочту")])
    userPassword = StringField(
        'Пароль', validators=[InputRequired(message="Введите свой пароль"),
                              Length(min=5, message="Пароль не должен быть короче 5 символов")])
    submit = SubmitField('Войти')
