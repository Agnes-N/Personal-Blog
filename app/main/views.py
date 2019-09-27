from flask import render_template,request,redirect,url_for,abort
from . import main
from app.requests import get_quotes
from flask_login import login_user,login_required,current_user
from ..models import Writer,Blog,Quotes,Article
from .. import db
import requests
from .. requests import get_quotes
from .forms import BlogForm

@main.route('/')
def index():

    
    blogs = Blog.query.all()
    quotes = get_quotes()
    return render_template('index.html', blogs = blogs,quotes = quotes)

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