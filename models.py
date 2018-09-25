from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    description = db.Column(db.String(264))
    choices = db.relationship('Choices', backref='pizza', lazy='dynamic')


class Choices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_title = db.Column(db.String(32))
    choice_price = db.Column(db.Numeric)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

