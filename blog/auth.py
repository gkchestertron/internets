from flask import Flask, request, session, g, redirect, flash, render_template, Blueprint
from models import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask_mail import Message, Mail
auth = Blueprint('auth', __name__)

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form.get('username')
		password = str(request.form.get('password'))
		user = User.from_username(username) 
		if user and user.login(password):
			session['user_id'] = user.id
			flash('You have successfully logged in!')
			return redirect('/')
		else:
			flash('Login Failed')
			return redirect('/login') 

@auth.route('/logout', methods=['POST'])
def logout():
	session['token'] = None
	return redirect('/')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	elif request.method == 'POST':
		try:
			username = request.form.get('username')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			email = request.form.get('email')
			confirm_email = request.form.get('confirm_email')
			if password != confirm_password:
				flash('Passwords do not match!')
			elif email != confirm_email:
				flash('Email address does not match')
			else:
				user = User.create(username, password, email)
				token = user.gentoken()
				link = 'http://localhost:5000/verify?token=' + token
				msg = Message('Signup works!',sender='tprobstcoding@gmail.com', recipients=[email])
				msg.body = link
				mail.send(msg)
				flash('Email Sent.')
		except IntegrityError:
			flash('That username is taken, please try again')
			db_rollback()
			return redirect('/signup')
		except InvalidRequestError:	
			db_rollback()
			return redirect('/signup')
		return redirect('/')

@auth.route('/verify', methods=['GET'])
def verify():
	token = request.args.get('token')
	user = User.from_token(token)
	if user:
		flash('Successful verification')
		user.verify()
		return redirect('/login')
	else:
		flash('Incorrect user')
		return redirect('/')

