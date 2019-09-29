from flask_wtf import  FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required, Email
from ..models import Subscription

class BlogForm(FlaskForm):
    title = StringField('Title',validators = [Required()])
    content = TextAreaField('Content',validators = [Required()])
    image = StringField('Image url',validators = [Required()])
    submit = SubmitField('submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[Required()])
    submit = SubmitField('Comment')

class UpdateBlogForm(FlaskForm):
    title = StringField('Title',validators = [Required()])
    content = TextAreaField('Content',validators = [Required()])
    image = StringField('Image url',validators = [Required()])
    submit = SubmitField('submit')

class SubscriptionForm(FlaskForm):
    name = StringField('Name', validators = [Required()])
    email = StringField('Email',validators=[Required(),Email()])
    submit = SubmitField('submit')

    def validate_email(self,data_field):
        if Subscription.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if Writer.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')