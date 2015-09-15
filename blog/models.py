from flask import g, session
from users import User
from posts import Post
from comments import Comment
from db import db

db.create_all()

def current_user():
	current_user = g.get('current_user')
	if not current_user:
		token = session.get('token')
		if token:
			current_user = User.from_token(token)
	g.current_user = current_user	
	return current_user

def db_add(data):
	db.session.add(data)
	db.session.commit()

def db_delete(data):
	db.session.delete(data)
	db.session.commit()

def db_rollback():
	db.session.rollback()