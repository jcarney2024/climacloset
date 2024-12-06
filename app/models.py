from flask_login import UserMixin
from . import db
from app import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    image_file = db.Column(db.String(130), nullable=False, default='default.jpg')
    name = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)

    
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
