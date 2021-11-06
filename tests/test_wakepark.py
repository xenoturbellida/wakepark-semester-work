from flask import url_for
from werkzeug.security import generate_password_hash

from wakepark.models import User


def login(client, email, password):
    return client.post('/login',
                       data=dict(email=email, password=password, submit='Зарегистрироваться'),
                       follow_redirects=True,
                       content_type='application/x-www-form-urlencoded')


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_logout(app_):
    """Make sure login and logout works."""
    with app_[0].test_client() as client:
        email = 'ivan@gmail.com'
        password = 'cool67password'

        login(client, email, password)

        new_user = User(email=email, password=generate_password_hash(password))
        tdb = app_.config['DATABASE']
        db_user = tdb.session.query(email=email).first()
        assert new_user == db_user
