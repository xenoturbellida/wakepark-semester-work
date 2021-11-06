class Config(object):
    TESTING = False
    SECRET_KEY = 'thisisasecretkey'
    WTF_CSRF_ENABLED = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'need to change'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tibobe78@localhost/wakepark'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tibobe78@localhost/wakepark_test'
    TESTING = True
    WTF_CSRF_ENABLED = True
