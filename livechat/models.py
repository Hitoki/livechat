import uuid

from flask.ext.login import unicode

from werkzeug.security import check_password_hash, generate_password_hash

from livechat import login_manager
from livechat import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    hash = db.Column(db.String(32), unique=True)
    livechat_login = db.Column(db.String(128), unique=True)
    livechat_api_key = db.Column(db.String(128), unique=True)
    websites = db.relationship('Website', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_user_data(self, data):
        if not self.hash:
            self.hash = uuid.uuid4().hex
        self.livechat_login = data.get('livechat_login')
        self.livechat_api_key = data.get('livechat_api_key')
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "livechat_login": self.livechat_login,
            "livechat_api_key": self.livechat_api_key
        }


class Website(db.Model):
    __tablename__ = 'website'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    google_track_id = db.Column(db.String(128), unique=True)
    group = db.Column(db.Integer)
    tags = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, google_track_id, group, tags):
        self.title = title
        self.google_track_id = google_track_id
        self.group = int(group)
        self.tags = tags

    def __repr__(self):
        return '<Website: {}>'.format(self.title)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)