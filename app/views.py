from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required

from app import app, db, lm
from .models import User

global_user= None
static_args= {
    'creator':'Marco',
    'latest':'1.5',
    'versions':[
        {'number':'1.0', 'date':'06-02-2016', 'comment':'init'},
        {'number':'1.1', 'date':'07-02-2016', 'comment':'Added file structure and basic "Hello Word"'},
        {'number':'1.2', 'date':'07-02-2016', 'comment':'Added template and Template logic'},
        {'number':'1.3', 'date':'07-02-2016', 'comment':'Added flask-WTF'},
        {'number':'1.4', 'date':'08-02-2016', 'comment':'Added LogIn system, Added scripts managing DB'},
        {'number':'1.5', 'date':'08-02-2016', 'comment':'Added Registration system'}
    ]
}

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    args= static_args
    return render_template('index.html',
                           title='(__hello word__)',
                           args=args), 200

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', args=static_args)
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', args=static_args)
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user