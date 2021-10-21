from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, length, ValidationError

from wakepark.models import User


class RegisterForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), length(min=4, max=40)],
        render_kw={"placeholder": 'Email'})

    password = PasswordField(
        validators=[InputRequired(), length(min=4,max=20)],
        render_kw={"placeholder": "Пароль"})

    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('Пользователь с таким именем уже существует. Пожалуйста, выберите другую почту.')


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), length(min=4, max=40)],
        render_kw={"placeholder": 'Email'})

    password = PasswordField(
        validators=[InputRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Пароль"})

    submit = SubmitField("Войти")

    remember_me = BooleanField(label='Запомнить меня')
