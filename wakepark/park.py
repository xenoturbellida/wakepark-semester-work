from flask import Flask, request, render_template, Blueprint

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import models



park = Flask(__name__)
db = SQLAlchemy(park)
park.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
park.config['SECRET_KEY'] = 'thisisasecretkey'
park.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
import forms

@park.route('/')
def index():
    return render_template('index.html')


@park.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = models.User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('signup.html', form=form)


@park.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    return render_template('login.html', form=form)


@park.route('/logout')
def logout():
    pass


if __name__ == '__main__':
    park.run(debug=True)
