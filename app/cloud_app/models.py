from datetime import datetime
from cloud_app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# each class is a model and also a table in the database
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	image_file = db.Column(db.String(20), default = 'default.jpg')
	password = db.Column(db.String(60), nullable = False)
	# not actually a column, is a query on the post table to grab posts by this users
	posts = db.relationship('Post', backref='author', lazy = True)


	def get_reset_token(self, expires_sec=1800):
		# serializer allows for token generation based on secret key of app
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		token = s.dumps({'user_id' : self.id}).decode('utf-8')
		return token


	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			# see if the token matches that generated from this user id
			user_id = s.loads(token)['user_id']
		except:
			return None

		return User.query.get(user_id)


	def __repr__(self):
		return "User: %s, %s, %s" % (self.username, self.email, self.image_file)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	# will put the current value of User.id in the user_id column
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	
	def __repr__(self):
		return "User: %s, %s" % (self.title, self.date_posted)
