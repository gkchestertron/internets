from flask import Flask, session, g, request, redirect, flash, render_template, Blueprint
from db import db
from models import *
import auth
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from functools import wraps

app = Flask(__name__)

app.config.from_object('config')

db.create_all() #Get rid of before production

def logged_in(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		if current_user():
			return func(*args, **kwargs)
		else:
			flash('You must be logged in')
			return redirect('/login')
	return decorated

#def is_admin()

@app.route('/')
def index():
	user = current_user()
	username = None
	if user:
		username = user.username
	return render_template('index.html', username=username, current_user=user, posts=Post.query.order_by(Post.id.desc()).all())

@app.route('/users', methods=['GET', 'POST'])
def users():
	if request.method == 'GET':
		return render_template('users.html', users=User.query.all())
	elif request.method == 'POST':
		name = request.form['name']
		user = User(name=name)
		db.session.add(user)
		db.session.commit()
		return redirect('/users')


@app.route('/posts', methods=['GET', 'POST'])
@logged_in
def posts():
	if request.method == 'GET':
		return render_template('posts.html', posts=Post.query.order_by(Post.id.desc()).all())
	elif request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		user_id = g.current_user.id
		post = Post(title=title, body=body, user_id=user_id)
		db.session.add(post)
		db.session.commit()
		return redirect('/posts')

@app.route('/comments', methods=['POST'])
@logged_in
def comments():
	body = request.form.get('body')
	post_id = request.form.get('post_id')
	user_id = g.current_user.id #TODO figure out what this means again, and how we incorporate the user id into this
	comment = Comment(body=body, post_id=post_id, user_id=user_id)
	db.session.add(comment)
	db.session.commit()
	print comment
	return redirect('/posts')

@app.route('/posts/delete', methods=['POST'])
#@logged_in change for admin??
def delete_posts():
	id = request.form['id']
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')



# register blueprints
app.register_blueprint(auth.auth, session=session, g=g)


if __name__ == '__main__':
	app.run()

