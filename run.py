from livechat import app, db
from livechat.models import User


db.create_all()

for user in app.congig.get('USERS'):
    if not User.query.filter_by(username=user[0]).first():
        new_user = User(username=user[0], password=user[1])
        db.session.add(new_user)
        db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

