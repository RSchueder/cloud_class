from flask import render_template, url_for, flash, redirect
from cloud_app import app
from cloud_app.forms import RegistrationForm, LoginForm
from cloud_app.models import User, Post


posts = [
	{'author' : 'Rudy',
	 'title' : 'blog post 1',
	 'content' : 'First post content',
	 'date_posted' : 'April 20, 2018'},


	{'author' : 'Jane',
	 'title' : 'my trip',
	 'content' : 'info about my trip',
	 'date_posted' : 'June 20, 2017'},
]

# home page
# two routes handled by the same function
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', posts = posts)


@app.route('/about')
def about():
	return render_template('about.html', title = 'About')


@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		# flash the messages, flashed messages are picked up in layout, and displayed
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))

	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')

	return render_template('login.html', title='Login', form=form)


