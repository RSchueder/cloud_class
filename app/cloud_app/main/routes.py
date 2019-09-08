from flask import Blueprint
from flask import render_template, request
from cloud_app.models import Post, Network
from flask import url_for, current_app
from cloud_app import db

import glob
import os

main = Blueprint('main', __name__)

# home page
# two routes handled by the same function
@main.route('/')
@main.route('/home')
def home():
	page = request.args.get('page', default = 1, type = int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 2)
	networks = Network.query.all()
	print(networks)
	if len(networks) < 1:
		print('adding networks')
		for mod in glob.glob(os.path.join(current_app.root_path, 'static', 'networks', '*.pth')):
			file = os.path.split(mod)[1]
			network = Network(name = file.replace('.pth',''), weights_file = file)
			db.session.add(network)
			db.session.commit()
	else:
		print('not adding networks')

	return render_template('home.html', posts = posts)


@main.route('/about')
def about():
	return render_template('about.html', title = 'About')
	