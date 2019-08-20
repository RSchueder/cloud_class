from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField('Upload cloud picture'  , validators=[FileAllowed(['jpg', 'png']), FileRequired([])])
    submit = SubmitField('Post')

