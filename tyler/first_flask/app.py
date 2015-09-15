from flask import Flask, render_template, request, redirect, session, flash
from models import Post, Comment, User, db
from sqlalchemy.exc import IntegrityError, InvalidRequestError 

app = Flask(__name__)   

# we now have an authetication system,
#HW:
#.5 build user page that shows users and add posts and comments or something interactive
#1 figure out how to validate email!!
#2 add verify password field!!(second password box to verify they enter the same password twice when signing up)
#3 add timestamps(in model layer)
#4----look into how flash messages work and how to use flash messages in flask!----

#Notes:
# data models concerned with data (more complicated logic)
# routes layer concerned with handling requests(shouldnt do user logic directly) handles requests
# verifying email should go into the controller layer(when request comes in check for valid email)



app.config.from_object('config')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('sign_up.html')
	elif request.method == 'POST':
		try:	
			username = request.form.get('username')
			password = request.form.get('password')
			User.create(username, password)
		except IntegrityError:
			flash('Username already exists please try again.')
			db.session.rollback()
			return redirect('/signup')
		except InvalidRequestError:
			db.session.rollback()
			return redirect('/signup')
		return redirect('/')

@app.route('/comments', methods=["POST"])
def comments():
	body = request.form.get("body")
	post_id = request.form.get("post_id")
	user_id = 1
	comment = Comment(body=body, post_id=post_id, user_id=user_id)
	db.session.add(comment)
	db.session.commit()
	return redirect('/posts')

@app.route('/posts', methods=["GET", "POST"])
def posts():
	if request.method == "GET":
		return render_template('posts.html', posts=Post.query.all())
	elif request.method == "POST":
		title = request.form.get('title')
		body = request.form.get('body')
		user_id = 1					#ask how to get a handle on the logged in user id from here
		Post.create(title, body, user_id)
		return redirect('/posts')

@app.route('/posts/delete', methods=["POST"])
def posts_delete():
	id = request.form.get('id')
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')

@app.route('/')		
def home():
	user_id = session.get('user_id')
	if user_id:
		user = User.query.get(user_id)
		username = user.username
	else:
		username = None
	return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		user = User.from_username(username)
		if user and user.verify_password(password):
			flash('You have logged in successfully')
			session['user_id'] = user.id
			return redirect('/')
		else:
			flash('Login Failed')
			return redirect('/login')

@app.route('/logout', methods=['POST'])
def logout():
	session['user_id'] = None
	flash('You have been logged out')
	return redirect('/')


if __name__ == '__main__':
	app.run() 