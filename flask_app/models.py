from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64
import pyotp


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    #masterPassword
    password = db.StringField(required=True)

    otp_secret = db.StringField(required = True, min_length = 16, default = pyotp.random_base32())

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class UserPasswords(db.Document):
    user = db.ReferenceField(User, required=True)
    app = db.StringField(required=True, min_length=1, max_length=500)
    appLink = db.StringField(required=False)
    username = db.StringField(required=True, min_length=1, max_length=40)
    password = db.StringField(required=True, min_length=1, max_length=100)
