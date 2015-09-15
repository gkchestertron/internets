from db import db


class Post(db.Model):
	__tablename__='posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), index=True, nullable=False)
	body = db.Column(db.Text(length=10000), index=True, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

	@classmethod
	def create(cls, title, body, category_id):
		try:
			post = Post(title=title, body=body, category_id=category_id)
			db.session.add(post)
			db.session.commit()
		except:
			db.session.rollback()
