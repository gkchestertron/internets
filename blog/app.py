from flask import Flask, session, g, request, render_template, flash, redirect
from models import *
import auth
from functools import wraps
#HW:! things to try: email verication, reset password, password retrieval *NEED HELP*
#SQLzoo.net if time look at this website to learn about SQL!
#HW!! START SOCIAL APP WITH AUTH implemented and folders for specific things, routes folder, models folder, 
# social/
# 	app.py	
# 	models/
# 	views/
# 	templates/
#	config.py(with git ignore)
# USE EMAIL INSTEAd of username

app = Flask(__name__)
app.config.from_object('config')


def logged_in(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		if current_user():
			return func(*args, **kwargs)
		else:
			flash('Please login!')
			return redirect('/login')
	return decorated


@app.route('/', methods=['GET'])
def home():
		user = current_user()
		username = None
		if user:
			username = user.username
		return render_template('home.html', username=username, current_user=user, posts=Post.query.order_by(Post.id.desc()).all())

@app.route('/posts', methods=['GET', 'POST']) #make posts have hashtags for searching function 
@logged_in
def posts():
	if request.method == 'GET':
		return render_template('posts.html', posts=Post.query.order_by(Post.id.desc()).all())
	elif request.method == 'POST':
		title = request.form.get('title')
		body = request.form.get('body')
		user = current_user()
		user_id = user.id
		post = Post(title=title, body=body, user_id=user_id)
		db_add(post)
		return redirect('/posts')

app.register_blueprint(auth.auth, session=session, g=g)


@app.route('/posts/delete', methods=['POST'])
@logged_in
def delete_posts():
	id = request.form.get('id')
	post = Post.query.get(id)
	db_delete(post)
	return redirect('/posts')

@app.route('/comments', methods=['POST'])
@logged_in
def comment():
	body = request.form.get('body')
	post_id = request.form.get('post_id')
	user_id = g.current_user.id
	comment = Comment(body=body, post_id=post_id, user_id=user_id)
	db_add(comment)
	return redirect('/')

if __name__ == '__main__':
	app.run()

