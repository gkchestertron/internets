from db import db

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	body = db.Column(db.String(1000), nullable=False)
	comments = db.relationship('Comment', backref='post', cascade='all, delete, delete-orphan')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))