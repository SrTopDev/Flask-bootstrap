from flask import Blueprint, render_template
from flask_login import login_required, current_user
from __init__ import db

main = Blueprint('main', __name__)

@main.route('/', methods=('GET', 'POST'))
@login_required
def index():
    return render_template('main.html', name=current_user.name)