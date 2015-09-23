#HW: importing files/pictures
#HW: start/finish sqlzoo, do codecademy CSS and HTML
#HW: look at javascript
#HW: image class  with relationship to post
#HW: Post will have images
#HW: images should have Filename, post_id, and id
#HW: interface for adding multiple images

#HW: look into jQuery and javascript: Codecademy


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
app.register_blueprint(posts.posts, session=session, g=g)

if __name__ == '__main__':
	app.run()
