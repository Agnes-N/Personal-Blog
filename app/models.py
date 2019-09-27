from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from datetime import datetime
datetime.utcnow()

@login_manager.user_loader
def load_user(writer_id):
    return Writer.query.get(int(writer_id))

class Writer(UserMixin,db.Model):

    __tablename__ = "writers"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True, index=True)

    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))

    blogs = db.relationship('Blog', backref='writer', lazy="dynamic")
    comments = db.relationship('Comment', backref='writer', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('you cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def save_writer(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Writer{self.username}'

class Blog(db.Model):

    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(500))
    image = db.Column(db.String(500))

    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'))
    comments = db.relationship('Comment', backref='blogs', lazy='dynamic')
   
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_blog(cls):
        Blog.blog.clear()
    
    @classmethod
    def get_blogs(cls):
        blog = Blog.query.all()
        return blog

    def delete(self, id):
        comments = Comment.query.filter_by(id = id).all()
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Blog {self.content}'



class Comment(db.Model):
    '''
    Comment class to define comment objects
    '''
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text())
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comment(self):
        Comment.comments.clear()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blog_id = id).all()
        return comments
    
    @classmethod
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comment{self.comment}'

class Quotes:
    '''
    Quote class to define quote objects
    '''

    def __init__(self,author,quote):

        self.author = author
        self.quote = quote