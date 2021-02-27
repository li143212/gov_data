
from flask_login import UserMixin
import sqlite3

class User(UserMixin):
    pass

def get_userdb():
    db = sqlite3.connect('user.db')
    db.row_factory = sqlite3.Row
    return db


def query_userdb(query, args=(), one=False):
    db = get_userdb()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv

users = query_userdb('SELECT * FROM users')

def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user





