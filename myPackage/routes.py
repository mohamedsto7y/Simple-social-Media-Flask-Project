from flask import render_template, url_for, redirect, flash, Blueprint
from myPackage import app,db
from myPackage.forms import RegistrationForm, LoginForm,PostForm
from myPackage.models import User, Post

# login imports
from flask_login import login_user, current_user, logout_user, login_required

# hashing password
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# blueprint
users = Blueprint(
	'users',
	__name__,
	url_prefix='/users'
)

# --------------------------- routes ---------------------------
# Decorator add functionality to functions without adding code
# (.route) Decorator handles all the complicated backend stuff
# to allow us to have a function for this specific route

# Homepage Endpoint
@app.route('/')
@app.route('/home')
def home():
	with app.app_context():
		query = db.session.query(
			Post,
			User
			)\
			.join(User, Post.user_id == User.id)\
			.order_by(Post.id.asc())\
			.all()

		# for record in query:
		# 	print(f"id : {record.Post.id}")
		# 	print(f"title : {record.Post.title}")
		# 	print(f"content : {record.Post.content}")
		# 	print(f"user email : {record.User.email}\n")
	return render_template('fb1.html', query=query, title="home page")		
	# with app.app_context():
	# 	users = User.query.all()
	# 	for user in users:
	# 		pass
	# 		#print(f"user is {user.username}")
	# 		for post in user.posts:
	# 			pass

		
		# for user in users:
		# 	print(f"user is {user.username}")
		# 	for post in user.posts:
		# 		print(f"Post : {post.title}")
		# 		print(f"Content : {post.content}")
	#return render_template('home.html', users=users, title="home page")

	# result = [
	# {
	# 	'student': 'yahia',
	# 	'grade': 10,
	# 	'year': 2021
	# },
	# {
	# 	'student': 'ahmed',
	# 	'grade': 20,
	# 	'year': 2020
	# },
	# {
	# 	'student': 'osama',
	# 	'grade': 30,
	# 	'year': 2019
	# }
	# ]
	# return render_template('home.html', result=result, title="home page")

# About Endpoint
@app.route('/about')
@login_required
def about():
	return render_template('about.html', title='about page')

# Redirect Endpoint
@app.route('/redirect')
def redirectFunc():
	return redirect(url_for('home'))

# Redirect Endpoint
@app.route('/test')
def test():
	result = [
	{
		'name': 'About page',
		'url': "about"
	},
	{
		'name': 'Home page',
		'url': "home"
	},
	]
	return render_template('test.html', result=result)

@users.route('/register', methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		with app.app_context():
			# pip install flask-bcrypt
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
			new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
			db.session.add(new_user)
			db.session.commit()
		flash(f"Registration Successfull {form.username.data}", "success")
		return redirect(url_for('users.login'))

	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
		

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		# if user exists , check his password
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			print(current_user.id)
			flash(f"Login Successfull {user.username}", "success")
			return redirect(url_for('home'))
		else:
			flash(f"Login Unsuccessfull", "danger")
			return render_template('login.html', title='Login', form=form)

	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/createpost',methods=['GET','POST'])
@login_required
def createpost():
	form=PostForm()
	if form.validate_on_submit():
		with app.app_context():
	# 	user = User.query.filter_by(username="mohamed").first()
	#	user = User.query.filter_by(id=current_user.id).first()
	 		post1 = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
	# 	post2 = Post(title='testtitle2', content='testcontent2', user_id=user.id)
	 		db.session.add(post1)
	# 	db.session.add(post2)
	 		db.session.commit()
		flash(f"Posted Successfull", "success")
		return redirect(url_for('home'))

	return render_template('crposts.html', title='crposts',form=form)



@app.route('/editpost/<int:int>', methods=['GET','POST'])
@login_required
def singlepost(int):
	post= Post.query.filter_by(id=int).first()
	form=PostForm(instance=post)
	if form.validate_on_submit():
		with app.app_context():
			#post.title=form.title.data
			post= Post.query.filter_by(id=int).update(dict(title=form.title.data,content=form.content.data))
			db.session.commit()
			flash(f"update Successfull", "success")
			return redirect(url_for('home'))
			#print(post.title)



		
	return render_template('singlepost.html', title='spost',post=post,form=form)

@app.route('/deletepost/<int:int>', methods=['GET','POST'])
def deletepost(int):
	with app.app_context():
		post= Post.query.filter_by(id=int).delete()
		db.session.commit()
		flash(f"delete Successfull", "success")
		return redirect(url_for('home'))


@app.route('/myprofile')
@login_required
def myprofile():
	with app.app_context():
		query = db.session.query(
			Post,
			User
			)\
			.join(User, Post.user_id == User.id)\
			.order_by(Post.id.asc())\
			.all()	
			# .filter_by(Post.user_id==int)
		# posts = Post.query.filter_by(user_id=int)
	return render_template('profile.html', query=query, title="profile")


@app.route('/profile/<int:int>')
@login_required
def profile(int):
	with app.app_context():
		query = db.session.query(
			Post,
			)\
			.join(User)\
			.filter(User.id == int)
		print(type(query))
		print(query)	
			# .filter_by(Post.user_id==int)
		# posts = Post.query.filter_by(user_id=int)
	return render_template('profile1.html', query=query, title="profile")		


