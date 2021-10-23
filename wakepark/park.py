from flask import Flask, request, render_template, Blueprint, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import models
from wakepark.cashier.cashier import cashier

park = Flask(__name__)
park.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
park.config['SECRET_KEY'] = 'thisisasecretkey'
park.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(park)

import forms

park.register_blueprint(cashier, url_prefix='/cashier')

login_manager = LoginManager()
login_manager.init_app(park)
login_manager.login_view = "login"




@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


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
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@park.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                remember = bool(form.remember_me.data)
                login_user(user, remember)
                return "successfull login"
    return render_template('login.html', form=form)


@park.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    park.run(debug=True)
