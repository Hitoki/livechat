import uuid
from flask.ext.login import unicode
from livechat import db
from werkzeug.security import check_password_hash, generate_password_hash
from livechat import login_manager


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    hash = db.Column(db.String(32), unique=True)
    google_track_id = db.Column(db.String(128), unique=True)
    livechat_login = db.Column(db.String(128), unique=True)
    livechat_api_key = db.Column(db.String(128), unique=True)

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
        self.google_track_id = data.get('google_track_id')
        self.livechat_login = data.get('livechat_login')
        self.livechat_api_key = data.get('livechat_api_key')
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)