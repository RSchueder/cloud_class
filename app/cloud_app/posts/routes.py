from flask import render_template, url_for, flash, redirect, request, abort
from cloud_app import db
from cloud_app.posts.forms import PostForm
from cloud_app.models import Post
from flask_login import current_user, login_required
from cloud_app.posts.utils import save_cloud_picture

from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		flash('Form was deemed valid', 'success')

		if form.picture.data:
			picture_file = save_cloud_picture(form.picture.data)
			post = Post(title = form.title.data, content = form.content.data, image_file = picture_file , author = current_user)

			db.session.add(post)
			db.session.commit()

			flash('Your post has been created!', 'success')
			return redirect(url_for('main.home'))
		else:
			flash('Picture upload failed, error is ' + str(form.picture), 'danger')
			return redirect(url_for('main.home'))
		
	return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('posts.post', post_id = post.id ))

	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content		

	return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted :(', 'success')
	return redirect(url_for('main.home'))



