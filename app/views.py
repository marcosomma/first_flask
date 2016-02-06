from app import app, Response

@app.route('/')
@app.route('/index')
def index():
    return Response(response="Hello World 1.0 !", status=200)