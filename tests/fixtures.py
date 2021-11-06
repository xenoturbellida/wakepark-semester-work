import pytest

from wakepark.config import TestingConfig
from wakepark.models import db
from wakepark.park import app


@pytest.fixture
def app_():
    app.config.from_object(TestingConfig())
    with app.app_context():
        db.create_all()
        yield app, db
        app.config['DATABASE'] = None
        db.session.remove()
        db.drop_all()
