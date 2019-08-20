import os

class Config():
    #SECRET_KEY              = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY='2dfb5258eda9b125e3252bfc43c71ed1'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

    MAIL_SERVER             = 'smtp.googlemail.com'
    MAIL_PORT               = 587
    MAIL_USE_TLS            = True
    MAIL_USERNAME           = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD           = os.environ.get('EMAIL_PASS')

    