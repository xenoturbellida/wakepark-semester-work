from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from wakepark.models import db, Post


def get_post(pubdate: str):
    datetime_ = datetime.fromisoformat(pubdate)
    try:
        post = db.session.query(Post).filter_by(pubdate=datetime_).first()
    except SQLAlchemyError as e:
        post = None
        print(e)
    return post
