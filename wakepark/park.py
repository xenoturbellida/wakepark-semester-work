from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError

from wakepark.cashier.cashier import cashier
from wakepark.config import DevelopmentConfig
from wakepark.editor.editor import editor
from wakepark.editor.helpers import ParkDatabase
from wakepark.forms import RegisterForm, LoginForm, ChangePasswordForm
from wakepark.helpers import get_post
from wakepark.models import db, User


login_manager = LoginManager()
login_manager.login_view = "login"
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig())

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.register_blueprint(cashier, url_prefix='/cashier')
    app.register_blueprint(editor, url_prefix='/editor')

    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index_without_page():
    return redirect(url_for('index', page=1))


@app.route('/<int:page>')
def index(page):
    pdb = ParkDatabase(db)
    posts = pdb.get_posts(page)
    pubdates = []
    for post in posts:
        pubdates.append(post[3].isoformat())
    return render_template('index.html',
                           posts=posts,
                           pubdates=pubdates,
                           page=page,
                           total_pages=pdb.get_total_pages(),
                           )


@app.route('/post/<pubdate>')
def post_content(pubdate):
    post = get_post(pubdate)
    return render_template('post.html',
                           title=post.title,
                           content=post.content,
                           photos=post.photos,
                           total_img=len(post.photos))


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
    return redirect(url_for("index_without_page"))


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
