from flask import Flask, g, session
from users import User
from posts import Post
from comments import Comment
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

def current_user():
	current_user = g.get('current_user')
	if not current_user:
		token = session.get('token')
		if token:
			current_user = User.from_token(token)
	g.current_user = current_user
	return current_user


'''def create_time(mapper, connection, instance):
	now = datetime.datetime.now()
	instance.created_at = now
	instance.updated_at = now

def update_time(mapper, connection, instance):
	now = datetime.datetime.now()
	instance.updated_at = now

def timestamp(cls):
	sa.event.listen(cls, 'before_insert', cls.create_time)
	sa.event.listen(cls, 'before_update', cls.update_time)'''
	
 