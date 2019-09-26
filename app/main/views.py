from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import Writer
from .. import db

@main.route('/')
def index():

    writers = Writer.query.all()

    return render_template('index.html', writers=writers)
