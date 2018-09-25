from flask import Flask, render_template, url_for, redirect, make_response, request
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


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        auth = request.authorization
        if not auth or (auth.username != app.config['BASIC_AUTH_USERNAME']
                        and auth.password != app.config['BASIC_AUTH_PASSWORD']):
            raise HTTPException('', Response(
                "Введите корректные имя пользователя и пароль!",
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True


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


if __name__ == "__main__":
    app.run()
