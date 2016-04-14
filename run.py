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


if __name__ == '__main__':
    app.run(host='0.0.0.0')

