from flask import Flask, request, session, g, redirect, flash, render_template, Blueprint
from datetime import datetime
from models import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from db import db
from flask_mail import Message, Mail

# create blueprint
auth = Blueprint("auth", __name__)

# get app object
app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	elif request.method == 'POST':
		try:
			username = request.form.get('username')
			email = request.form.get('email')
			confirm_email = request.form.get('confirm_email')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			if password != confirm_password:
				flash('passwords do not match')
			elif email != confirm_email:
				flash('email addresses do not match')
			else:
				user = User.create(username, password)
				token = user.generate_token()
				link = 'http://localhost:5000/verify?token=' + token
				msg = Message('Signup works!', sender='emscancode@gmail.com', recipients=['emscancode@gmail.com'])
				msg.body = link
				mail.send(msg)
				flash('Email Sent.')
		except IntegrityError:
			flash('That username/email is taken, please try again')
			db.session.rollback()
			return redirect('/signup')
		except InvalidRequestError:
			flash('I\'m sorry, something went wrong, please try again')
			db.session.rollback
			return redirect('/signup')
		return redirect('/')

@auth.route('/login', methods=['GET', 'POST'])
def login(): #don't need email for login
	error = None
	if request.method =='GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form.get('username')
		#email = request.form.get('email')
		password = request.form.get('password')
		user = User.from_username(username)
		valid_login = user and user.login(password)
		if valid_login:
			session['user_id'] = user.id
			flash('You were successfully logged in!')
			return redirect('/')
		else:
			flash('Login failed. Please try again.')
			return redirect('/login')

@auth.route('/logout', methods=['POST'])
def logout():
	session['token'] = None
	flash('You have been logged out')
	return redirect('/')

@auth.route('/verify', methods=['GET'])
def verify():
	token = request.args.get('token')
	user = User.from_token(token)
	if user:
		flash('You have been verified')
		user.verify()
		return redirect('/login')
	else:
		flash('Incorrect link')
	return redirect('/')


