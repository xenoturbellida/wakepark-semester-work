from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError

from wakepark.cashier.cashier import cashier
from wakepark.editor.editor import editor
from wakepark.forms import RegisterForm, LoginForm, ChangePasswordForm
from wakepark.models import db, User

# DATABASE = 'database.db'
DATABASE = 'wakepark.db'
DEBUG = True
SECRET_KEY = 'thisisasecretkey'
EXPLAIN_TEMPLATE_LOADING = False

app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tibobe78@localhost/wakepark'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(cashier, url_prefix='/cashier')
app.register_blueprint(editor, url_prefix='/editor')
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # TODO
    form = LoginForm()
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт')
        return render_template('login.html', form=form)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    remember = bool(form.remember_me.data)
                    login_user(user, remember)
                    return "successful login"
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if (form.validate_on_submit()
            and check_password_hash(current_user.password, form.old_password.data)
            and form.new_password.data == form.confirm_new_password.data):
        hashed_password = generate_password_hash(form.new_password.data)
        db.session.execute(update(User).where(User.id == current_user.get_id()).values(password=hashed_password))
        db.session.commit()
        flash('Пароль успешно изменён', category='success')
        return redirect(url_for('profile'))
    return render_template('security.html', form=form)


@app.route('/check_email', methods=['POST'])
def check_if_email_is_unique():
    form = RegisterForm()
    message = 'Email свободен'
    category = 'validationSuccess'
    try:
        form.validate_email(form.email)
    except ValidationError as e:
        message = str(e)
        category = 'validationError'
    return jsonify(message=message, category=category)


if __name__ == '__main__':
    app.run(debug=True)
