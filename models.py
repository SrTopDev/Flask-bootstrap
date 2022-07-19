from __init__ import db, app
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    email_confirm = db.Column(db.Boolean, default=False, nullable=False)



#It should uncomment when new table enter#
db.create_all(app=app)

