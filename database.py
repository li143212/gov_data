# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    psw = db.Column(db.String(20))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    user1 = User(username='Tom', psw='111111')
    user2 = User(username='Michael', psw='123456')

    db.session.add_all([user1, user2])
    db.session.commit()