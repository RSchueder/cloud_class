from flask import Blueprint, render_template

info = Blueprint('info', __name__)

# info pages
cloud_types = {'stratiform'       : ['cirrostratus', 'altostratus', 'stratus', 'nimbostratus'],
               'cirriform'        : ['cirrus'],
               'stratocumuliform' : ['cirrocumulus', 'altocumulus', 'stratocumulus'],
               'cumuliform'       : ['cumulus'],
               'cumulonimbiform'  : ['cumulonimbus']}
			   
@info.route('/info/clouds')
def clouds():
	return render_template('cloud_info.html', title = 'Cloud Info')


@info.route('/info/models')
def models():
	return render_template('model_info.html', title = 'Model Info')
	