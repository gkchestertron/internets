from flask import Flask, Blueprint, render_template, flash, redirect, request
from models import *
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.from_object('config')

cat = Blueprint('cat', __name__)

mail = Mail(app)

@cat.route('/categories', methods=['GET', 'POST'])
def categories():
	if request.method == 'GET':
		return render_template('categories.html', categories=Category.query.all())
	elif request.method == 'POST':
		pass

@cat.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template('create.html', categories=Category.query.all())
	elif request.method == 'POST':
		title = request.form.get('title')
		body = request.form.get('body')
		category_id = request.form.get('category_id')
		email = request.form.get('email')
		# token = bcrypt.gensalt()
		# link = 'http://localhost:5000/verify?token=' + token
		# msg = Message('email works!', sender='tprobstcoding@gmail.com', recipients=['tprobstcoding@gmail.com'])
		# msg.body = link
		# mail.send(msg)
		# flash('Confirmation email sent.')
		Post.create(title, body, category_id)
		flash('Post was successfully created')
		return redirect('/')

@cat.route('/posts', methods=['GET', 'POST'])
def posts():
	if request.method == 'GET':
		return render_template('posts.html', posts=Post.query.all())
	elif request.method == 'POST':
		pass





