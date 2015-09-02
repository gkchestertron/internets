from db import db

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True, index=True, nullable=False)
	password_hash = db.Column(db.String(255), index=True, nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False)
	posts = db.relationship('Post', backref='user')
	comments = db.relationship('Comment', backref='user')