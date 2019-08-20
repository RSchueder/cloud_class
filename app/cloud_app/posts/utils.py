import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_cloud_picture(form_picture):
	'''
	saves uploaded image to static folder and returns new path
	'''
	random_hex = secrets.token_hex(8)
	_ , f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/cloud_pics', picture_fn)
	
	# resize
	output_size = (256, 256)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn