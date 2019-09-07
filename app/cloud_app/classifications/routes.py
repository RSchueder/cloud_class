'''
in the same way that a user can have posts, posts can have classifications

'''

from cloud_app.classifications.utils import predict

@classifications.route('/post/<int:post_id>/classify', methods = ['POST'])
@login_required
def classify_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
    # for example
    cloud = predict('resnet34', post.image_file)

    