from flask import Flask, render_template, request, redirect, session, flash
from models import User, Person, Post, Comment, db
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import datetime

app = Flask(__name__) #name of program you're running (a system thing)

app.config.from_object('config')

@app.route('/persons', methods=['GET', 'POST'])
def persons():
	if request.method == 'GET':
		return render_template('persons.html', persons=Person.query.all())
	elif request.method == 'POST':
		name = request.form.get('name')
		person = Person(name=name)
		db.session.add(person)
		db.session.commit()
		return redirect('/persons')

@app.route('/') #decorator: associates this function with that route in the router
def home():
	user_id = session.get('user_id')
	if user_id:
		user = User.query.get(user_id)
		username = user.username
	else:
		username = None
	return render_template('home.html', username=username) #uses jinja2 

@app.route('/posts', methods=['GET', 'POST'])
def posts():
	if request.method == 'GET':
		return render_template('posts.html', posts=Post.query.all())
	elif request.method == 'POST':
		title = request.form.get('title')
		body = request.form.get('body')
		person_id = 1
		post = Post(title=title, body=body, person_id=person_id)
		db.session.add(post)
		db.session.commit()
		return redirect('/posts')

@app.route('/posts/delete', methods=['POST'])
def delete_posts():
	id = request.form.get('id')
	#Post.query.filter(Post.id=id)
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')

@app.route('/comments', methods=['POST'])
def comments():
	body = request.form.get('body')
	post_id = request.form.get('post_id')
	person_id = 1
	comment = Comment(body=body, post_id=post_id, person_id=person_id)
	db.session.add(comment)
	db.session.commit()
	return redirect('/posts')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form.get('username')
		password = str(request.form.get('password'))
		user = User.from_username(username)
		if user and user.verify_password(password):
			session['user_id'] = user.id
			flash('You were successfully logged in!')
			return redirect('/')
		else:
			flash('log in failed')
			return redirect ('/login')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
	if request.method == 'GET':
		return render_template('sign_up.html')
	elif request.method == 'POST':
		try:
			username = request.form.get('username')
			password = request.form.get('password')
			User.create(username, password)
		except IntegrityError:
			flash('That username is taken, please try again')
			db.session.rollback()
			return redirect('/sign_up')
		except InvalidRequestError:
			db.session.rollback()
			return redirect('/sign_up')
		return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
	session['user_id'] = None
	flash('You have been logged out')
	return redirect('/')

if __name__ == '__main__':
	app.run()


