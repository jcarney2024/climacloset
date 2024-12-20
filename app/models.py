from flask_login import UserMixin
from . import db
from app import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    image_file = db.Column(db.String(255), nullable=False, default='../static/default.png')

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    response = db.Column(db.String(255), nullable=False)
    
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
