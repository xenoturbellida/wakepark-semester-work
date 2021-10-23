from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    # def is_active(self):
    #     """True, as all users are active."""
    #     return True
    #
    # def get_id(self):
    #     """Return the email address to satify Flask-Login's requirements."""
    #     return self.email
    #
    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated
    #
    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False

