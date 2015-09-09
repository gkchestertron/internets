from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb
import datetime
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://north:starwars@localhost/north_bay'
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), nullable=False, unique=True, index=True)
	password_hash = db.Column(db.String(255))

	def verify_password(self, password):
		return bcrypt.hashpw(password.encode('utf-8'), self.password_hash.encode('utf=8')) == self.password_hash

	@classmethod
	def from_username(cls, username):
		return cls.query.filter(cls.username == username).first()

	@classmethod
	def create(cls, username, password):
		password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		user = cls(username=username, password_hash=password_hash)
		db.session.add(user)
		db.session.commit()

class Person(db.Model):
	__tablename__ = 'persons'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	posts = db.relationship('Post', backref='person')
	comments = db.relationship('Comment', backref='person')

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
	title = db.Column(db.String(255))
	body = db.Column(db.String(1000))
	comments = db.relationship('Comment', backref='post', cascade='all, delete, delete-orphan')
	timestamp = datetime.datetime.now()

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
	body = db.Column(db.String(1000))

db.create_all()


#db.session(.......)