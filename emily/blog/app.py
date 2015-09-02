from flask import Flask
from db import db
from models import *

app = Flask(__name__)

app.config.from_object('config')
db.app = app
db.init_app(app)

db.create_all() #Get rid of before production

@app.route('/')
def index():
	return 'Hello World'




if __name__ == '__main__':
	app.run()