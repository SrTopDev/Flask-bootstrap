from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
app = Flask(__name__)

from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import models

Bootstrap5(app)
# app.config.from_pyfile('config.py')

app.config['SECRET_KEY'] = "sadmaspinmdiasjdfohasiondiasmdopmasso"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"

db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)


from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer('Thisisasecret!')
mail = Mail(app)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = models.User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))
    new_user = models.User(email=email, name=name, password=generate_password_hash(password, method='sha256'), email_confirm=False)
    
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='info@flaskapp.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    print(email)
    user = db.session.query(models.User).filter_by(email=email).update({"email_confirm":True})
    db.session.commit()
    return redirect(url_for('main.index'))




if __name__ == '__main__':
    app.run(debug=True)
    