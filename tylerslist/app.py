#HW register an app on Facebook, search for facebook developers
#todo:  

from flask import Flask, render_template, Blueprint, session, g	
from models import *
from blueprints import *

app = Flask(__name__)
app.config.from_object('config')



@app.route('/')
def home():
	return render_template('home.html')

app.register_blueprint(categories.cat, session=session, g=g)
app.register_blueprint(auth.auth, session=session, g=g)

if __name__ == '__main__':
	app.run()
