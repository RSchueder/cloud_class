from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from cloud_app import db, bcrypt
from cloud_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from cloud_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from cloud_app.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		# flash the messages, flashed messages are picked up in layout, and displayed
		flash(f'Your account has been created! You can now login.', 'success')
		return redirect(url_for('users.login'))

	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit(): # if the form is filled in well
		user = User.query.filter_by(email = form.email.data).first() # look up user in databse
		if user and bcrypt.check_password_hash(user.password, form.password.data): #if user exists and password is correct
			login_user(user, remember = form.remember.data)
			# obtains page user was trying to go to when/if they were redirected here, for example if they went to 'account' 
			# without being logged in first
			next_page = request.args.get('next') 
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')

	return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods = ['GET', 'POST'])
@login_required 
# decorated with login_required. Cannot go to this page if not logged in
# if not logged in, then the login_managetr will redirect to the page it knows is the login page,
# which was specified in __init__.py as = login_manager.login_view = 'login' 
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file

		# I guess current user is known from login_user, and this is connected to the database
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', image_file = image_file, form = form)


@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', default = 1, type = int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
			.order_by(Post.date_posted.desc())\
			.paginate(page = page, per_page = 1)

	return render_template('user_posts.html', posts = posts, user = user)


@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))

	return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/request_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or old (expired) token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()

	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pw
		db.session.commit()
		flash(f'Your password has been reset.', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)