from flask import Flask, Response, render_template

from flask.ext.login import LoginManager, UserMixin, login_required


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

from app import views, form