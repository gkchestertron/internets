from flask import Flask, session, g
from db import db
from datetime import datetime
import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

app = Flask(__name__)
app.config.from_object('config')

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True, index=True, nullable=False)
	#email = db.Column(db.String(255), unique=True, index=True, nullable=False)
	password_hash = db.Column(db.String(255), index=True, nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False)
	posts = db.relationship('Post', backref='user')
	comments = db.relationship('Comment', backref='user')
	verified = db.Column(db.Boolean, default=False, nullable=False)

	def login(self, password):
		if self.verify_password(password) and self.verified:
			token = self.generate_token()
			session['token'] = token
			g.current_user = self
			return True
		return None

	def generate_token(self):
		serializer = Serializer(app.config['SECRET_KEY'], expires_in=3600)
		return serializer.dumps({'user_id': self.id})

	def verify_password(self, password):
		return bcrypt.hashpw(password.encode('utf-8'), self.password_hash.encode('utf-8')) == self.password_hash

	def verify(self):
		self.verified = True
		try:
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()

	#def verify_email(self, email):
		#pass #TODO?? how do I verify email?

	@classmethod
	def from_username(cls, username):
		return cls.query.filter(cls.username == username).first()

	@classmethod
	def create(cls, username, password):
		password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		#email = email #TODO!!!
		user = cls(username=username, password_hash=password_hash)
		db.session.add(user)
		db.session.commit()
		return user

	@classmethod
	def from_token(cls, token):
		serializer = Serializer(app.config['SECRET_KEY'])
		try:
			data = serializer.loads(token)
		except SignatureExpired, BadSignature:
			return None
		if data['user_id']:
			return cls.query.get(data['user_id'])
		return None


