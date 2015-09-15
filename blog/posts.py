from db import db

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	body = db.Column(db.String(255), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	comments = db.relationship('Comment', backref='post', cascade='all, delete, delete-orphan')
	# create_time = #create time stamp Use mysql (datetime type for mysql?)
	# update_time =

	