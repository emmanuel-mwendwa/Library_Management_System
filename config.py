import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECORDS_PER_PAGE = int(os.environ.get('RECORDS_PER_PAGE', 18))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


config = {
    "development": DevelopmentConfig,

    "default": DevelopmentConfig
}