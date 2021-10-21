from flask import Flask, request, render_template, Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


park = Flask(__name__)
db = SQLAlchemy(park)
park.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
park.config['SECRET_KEY'] = 'thisisasecretkey'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# login_manager = LoginManager()


@park.route('/')
def index():
    pass


@park.route('/signup', methods=['GET', 'POST'])
def signup():
    pass


@park.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@park.route('/logout')
def logout():
    pass


if __name__ == '__main__':
    park.run(debug=True)
