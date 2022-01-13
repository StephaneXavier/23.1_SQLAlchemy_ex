from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import backref
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)





class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(300), default='https://cdn-icons-png.flaticon.com/512/18/18601.png')

    def __repr__(self):
       return f'<{self.first_name} {self.last_name}>'
    


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    user_relationship = db.relationship('User',backref='posts')

   