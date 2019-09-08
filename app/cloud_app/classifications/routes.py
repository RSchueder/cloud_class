'''
in the same way that a user can have posts, posts can have classifications

'''

from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from cloud_app import db
from cloud_app.models import Post, Classification, Network
from flask_login import current_user, login_required
import datetime
from cloud_app.classifications.utils import predict

classifications = Blueprint('classifications', __name__)


@classifications.route('/post/<int:post_id>/set_classify', methods = ['POST', 'GET'])
@login_required
def set_classify_post(post_id):
	post = Post.query.get_or_404(post_id)
	networks = Network.query.all()
	
	if post.author != current_user:
		abort(403)

	return render_template('set_classify.html', post = post, networks = networks)
    

@classifications.route('/post/<int:post_id>/classify', methods = ['POST', 'GET'])
@login_required
def classify_post(post_id):
	network_id = request.args.get('network_id')

	post = Post.query.get_or_404(post_id)
	model = Network.query.get_or_404(network_id)

	if post.author != current_user:
		abort(403)
    # for example
	weights_file = url_for('static', filename = 'networks/' + model.weights_file)
	image_file = url_for('static', filename = 'cloud_pics/' + post.image_file)
	cloud = predict(weights_file, image_file)
	
	classification = Classification(result = cloud, date_run = datetime.datetime.utcnow, network = model.name, subject = post)
	db.session.add(classification)
	db.session.commit()

	return redirect(url_for('posts.post', post_id = post.id ))


    