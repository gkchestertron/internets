from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://north:starwars@127.0.0.1/north_bay'
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'people'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)

    def __repr__(self):
        return str(self.id) + ': ' + str(self.name)
