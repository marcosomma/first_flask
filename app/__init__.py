from flask import Flask, Response, render_template, flash, redirect

from flask.ext.login import LoginManager, UserMixin, login_required
from flask.ext.wtf import Form


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

from app import views, form