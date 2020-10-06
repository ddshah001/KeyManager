class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "HelloSecret"
    SECURITY_PASSWORD_SALT = "asduinuaisbdcaspvauhctfaxyubduycqwe"
    MAIL_DEFAULT_SENDER= 'demo@yourmail.com'
    MAIL_SERVER= 'mail.yourmail.com'
    MAIL_PORT= 26
    MAIL_USERNAME= 'demo@yourmail.com'
    MAIL_PASSWORD= 'your_mail_password'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= False

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