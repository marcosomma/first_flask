from app import *
from .form import LoginForm

global_user= None
static_args= {
    'creator':'Marco',
    'latest':'1.3',
    'versions':[
        {'number':'1.0', 'date':'06-02-2016', 'comment':'init'},
        {'number':'1.1', 'date':'07-02-2016', 'comment':'Added file structure and basic "Hello Word"'},
        {'number':'1.2', 'date':'07-02-2016', 'comment':'Added template and Template logic'},
        {'number':'1.3', 'date':'07-02-2016', 'comment':'Added flask-WTF'}
    ]
}

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    args= static_args
    return render_template('index.html',
                           title='(__hello word__)',
                           args=args), 200

@app.route('/login/', methods=['GET', 'POST'])
def login():
    args = static_args
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    content = {
        'test':'Testo con questo Testo il mio Test',
        'form':form,
        'providers':app.config['OPENID_PROVIDERS']
    }
    return render_template('login.html',
                           args=args,
                           content=content), 200

@app.route("/protected/" , methods=["GET", "POST"])
@login_required
def protected():
    return Response(response="Hello {0}! Welcome to Protected World 1.1!".format(global_user.id), status=200)
