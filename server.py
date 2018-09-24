from flask import Flask, render_template, g, url_for, redirect, make_response, request
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate
from config import Config
from functools import wraps
from flask import request, Response
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from models import Pizza, Choices, db
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth
from flask_admin.contrib import sqla
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
basic_auth = BasicAuth(app)


# def auth_requires(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if auth and auth.username == 'username' and auth.password == 'password':
#         # if auth and auth.username == app.config['BASIC_AUTH_USERNAME'] \
#         #         and auth.password == app.config['BASIC_AUTH_PASSWORD']:
#             return f(*args, **kwargs)
#         return make_response('Could not verify your access level for that URL.\n'
#                              'You have to login with proper credentials', 401,
#                              {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
#     return decorated

class MyModelView(sqla.ModelView):


    def is_accessible(self):
        auth = request.authorization
        if not auth or (auth.username != 'username' and auth.password != 'password'):
            #print(auth)
            #print(auth.username)
            # return  make_response('Could not verify your access level for that URL.\n'
            #                  'You have to login with proper credentials', 401,
            #                  {'WWW-Authenticate': 'Basic realm="Login Required"'})
            raise HTTPException('', Response(
                "Введите корректные имя пользователя и пароль!",
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        print('HERE')
        return True
#
#     @expose('/')
#     @expose('/admin')
#     def index(self):
#         return self.render('index.html')
#
#     # def __init__(self, session):
#     #     super(MicroBlogModelView, self).__init__(Pizza, session)

class PizzaView(MyModelView):
    column_searchable_list = ['title']
    column_labels = dict(title='Название',
                         description='Описание',
                         choices='Варианты')

class ChoicesView(MyModelView):
    column_searchable_list = ['choice_title']
    column_labels = dict(choice_title='Название',
                         choice_price='Цена')


admin = Admin(app, name='pizzeria', template_mode='bootstrap3')

admin.add_view(PizzaView(Pizza, db.session))
admin.add_view(ChoicesView(Choices, db.session))


# @app.route('/')
# @basic_auth.required
# def secret_view():
#     return render_template('index.html')


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
