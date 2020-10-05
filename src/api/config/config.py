class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "HelloSecret"
    SECURITY_PASSWORD_SALT = "asduinuaisbdcaspvauhctfaxyubduycqwe"
    MAIL_DEFAULT_SENDER= 'your_email_address'
    MAIL_SERVER= 'email_providers_smtp_address'
    MAIL_PORT= <mail_server_port>
    MAIL_USERNAME= 'your_email_address'
    MAIL_PASSWORD= 'your_email_password'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True

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