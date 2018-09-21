from flask import Flask, render_template, g, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate
from config import Config
from functools import wraps
from flask import request, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Pizza, Choices, db
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

admin = Admin(app, name='pizzeria', template_mode='bootstrap3')
admin.add_view(ModelView(Pizza, db.session))
admin.add_view(ModelView(Choices, db.session))


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secrets'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})



def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('admin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@requires_auth
def secret_page():

    return render_template('admin/index.html')



if __name__ == "__main__":
    app.run()
