from flask import render_template,request,redirect,flash,url_for,abort
from . import main
from app.requests import get_quotes
from flask_login import login_user,login_required,current_user
from ..models import Writer,Blog,Quotes,Comment,Subscription
from .. import db
import requests
from .. requests import get_quotes
from .forms import BlogForm,CommentForm,UpdateBlogForm,SubscriptionForm
from ..subscriber import mail_message

@main.route('/', methods=['GET','POST'])
def index():

    blogs = Blog.query.all()
    quotes = get_quotes()

    form = SubscriptionForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        subscriber = Subscription(name = name, email = email)
        db.session.add(subscriber)
        db.session.commit()
        
        return redirect(url_for('main.index'))
        mail_message("Welcome to my personal blog","subscriber/subscriber_user",subscriber.email,subscriber = subscriber)

    return render_template('index.html', blogs = blogs,quotes = quotes, form = form)

@main.route('/about')
def about():

    title = 'Welcome to my personal blog'

    return render_template('about.html', title = title)

@main.route('/create_new',methods=['GET','POST'])
@login_required
def new_blog():

    form = BlogForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        image = form.image.data
        writer_id = current_user

        new_blog_object = Blog(content = content,title = title, writer_id=current_user._get_current_object().id,image = image)
        new_blog_object.save_blog()

        return redirect(url_for('main.index'))
    return render_template('create_blog.html',form=form)

@main.route('/comment/<int:blog_id>', methods=['GET','POST'])
def comment(blog_id):

    form = CommentForm()
    blogs = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id=blog_id).all()

    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        # Writer_id = Writer_id
        writer_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,blog_id = blog_id,writer_id = writer_id)
        new_comment.save_comments()
        
        return redirect(url_for('.comment',blog_id = blog_id))
    return render_template('comment.html',form = form,blogs = blogs,comments = comments)

@main.route('/index/<int:id>/delete', methods = ['GET','POST'])
@login_required
def delete(id):
    current_post = Blog.query.filter_by(id = id).first()

    if current_post.writer != current_user:
        abort(404)
    db.session.delete(current_post)
    db.session.commit()
    return redirect(url_for('.index'))

@main.route('/index/<int:id>/delete_comment', methods = ['GET','POST'])
@login_required
def delete_comment(id):

    current_post = Comment.query.filter_by(id = id).first()

    if current_post.writer != current_user:
        abort(404)

    db.session.delete(current_post)
    db.session.commit()
    return redirect(url_for('.index'))
    return render_template('comment.html',current_post = current_post)


@main.route('/update/<int:id>',methods= ['GET','POST'])
@login_required
def update_blog(id):

    blogs = Blog.query.filter_by(id = id).first()
    if blogs is None:
        abort(404)

    form = UpdateBlogForm()

    if form.validate_on_submit():

        blogs.title = form.title.data
        blogs.content = form.content.data

        db.session.add(blogs)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('update_blog.html',form = form)