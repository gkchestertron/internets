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

@cat.route('/categories/<path:catname>')
def category(catname):
	category = Category.query.filter(Category.name==catname).first()
	return render_template('category.html', category=category)







