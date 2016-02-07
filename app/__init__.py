import os
from flask import Flask, Response, render_template, flash, redirect, g

from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, forms