from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from datetime import datetime

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
