from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default_avatar.jpg')
    date_creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reputation = db.Column(db.Integer, index = True, default=0)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=True)
    description = db.Column(db.String(5000), index=True, unique=False)
    author = db.Column(db.String(64), default=None, unique=False)
    image_file = db.Column(db.String(20), nullable=False, default='petite_fleur.png')
    #sauvegarde des images dans la bdd nécessaire a implementer
    quantity = db.Column(db.Integer, default=0, unique=False)

    
    def __repr__(self):
        return '<Plant {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))