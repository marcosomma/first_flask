from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import *
from .models import User
from .forms import LoginForm

global_user= None
static_args= {
    'creator':'Marco',
    'latest':'1.4',
    'versions':[
        {'number':'1.0', 'date':'06-02-2016', 'comment':'init'},
        {'number':'1.1', 'date':'07-02-2016', 'comment':'Added file structure and basic "Hello Word"'},
        {'number':'1.2', 'date':'07-02-2016', 'comment':'Added template and Template logic'},
        {'number':'1.3', 'date':'07-02-2016', 'comment':'Added flask-WTF'},
        {'number':'1.4', 'date':'08-02-2016', 'comment':'Added LogIn system, Added scripts managing DB'}
    ]
}

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = g.user
    args= static_args
    return render_template('index.html',
                           title='(__hello word__)',
                           args=args,
                           user=user), 200

@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    args = static_args
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    content = {
        'test':'Testo con questo Testo il mio Test',
        'form':form,
        'providers':app.config['OPENID_PROVIDERS']
    }
    return render_template('login.html',
                           args=args,
                           content=content), 200

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
