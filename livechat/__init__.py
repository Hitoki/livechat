from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


__all__ = ['app']

app = Flask(__name__)
app.config.from_object('livechat.settings.DevelopmentConfig')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

import livechat.views