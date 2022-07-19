from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import models
from __init__ import db, app


auth = Blueprint('auth', __name__)




@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = models.User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    if user.email_confirm == False:
        flash('Email is not verifired')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    return redirect(url_for('main.index'))





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))