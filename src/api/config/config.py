class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://keymanager:acyfgbafxbfuUYXF@localhost:3306/keymanager"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://keymanager:acyfgbafxbfuUYXF@localhost:3306/keymanager"
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://keymanager:acyfgbafxbfuUYXF@localhost:3306/keymanager"
    SQLALCHEMY_ECHO = False