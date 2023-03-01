# pip install flask-sqlalchemy
from myPackage import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	# max length for username is 20
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	profile_image = db.Column(db.String(120))
	# relationship between User and Post class
	# lazy loads the data only on demand
	# this column does not exist, this is just an additional query
	posts = db.relationship('Post', backref='author', lazy=True)

	# magic method to print user
	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	content = db.Column(db.Text, nullable=False)
	# table = lowercase, class = uppercase
	# table = data , class = python code
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# magic method to print post
	def __repr__(self):
		return f"Post('{self.title}', '{self.content}')"