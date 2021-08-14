import os, yaml
from reluni_review import db, datetime, bcrypt, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from reluni_review.config import Config

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=50), unique=True, nullable=False)
    email_address = db.Column(db.String(length=60), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(Config.config["secret_key"], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.config["secret_key"])

        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)


    @property
    def password(self):
        return self.password

    @password.setter # hashes password
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password): # checks whether hashed passwords are matched or not
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email_address}', '{self.password_hash}', '{self.posts}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=120), nullable=False, unique=True)
    content = db.Column(db.String(length=20480), nullable=False, unique=True)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.user_id}', '{self.title}', '{self.content}', '{self.time_stamp}')"
