from flask import Flask, render_template
from models import Person

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('home.html', data='this is some data')

@app.route('/people')
def people():
    return render_template('people.html', people=Person.query.all())

if __name__ == '__main__':
    app.run()
