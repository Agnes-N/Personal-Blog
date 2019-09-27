from flask_wtf import  FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField('Title',validators = [Required()])
    content = TextAreaField('Content',validators = [Required()])
    image = StringField('Image url',validators = [Required()])
    submit = SubmitField('submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[Required()])
    submit = SubmitField('Comment')