from app import *
from models import User

global_user= None
static_args= {
    'creator':'Marco',
    'latest':'1.2',
    'versions':[
        {'number':'1.0', 'date':'06-02-2016'},
        {'number':'1.1', 'date':'07-02-2016'},
        {'number':'1.2', 'date':'07-02-2016'}
    ]
}

@login_manager.request_loader
def load_user(request):
    global global_user
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":")
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                global_user = user
                return user
    return None

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    args= static_args
    return render_template('index.html',
                           title='(__hello word__)',
                           args=args), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    args = static_args
    content = {
        'test':'Testo con questo Testo il mio Test'
    }
    return render_template('login.html',
                           args=args,
                           content=content), 200

@app.route("/protected/" , methods=["GET", "POST"])
@login_required
def protected():
    return Response(response="Hello {0}! Welcome to Protected World 1.1!".format(global_user.id), status=200)
