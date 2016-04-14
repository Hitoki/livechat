import logging
from logging.handlers import RotatingFileHandler

from livechat import app, db
from livechat.models import User


db.create_all()
if not User.query.filter_by(username='admin').first():
    admin = User(username='admin', password='admin')
    db.session.add(admin)
    db.session.commit()


if not User.query.filter_by(username='test').first():
    test = User(username='test', password='test')
    db.session.add(test)
    db.session.commit()


handler = RotatingFileHandler('webhook.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

