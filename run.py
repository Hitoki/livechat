from livechat import app, db
from livechat.models import User

app.run(host='0.0.0.0', debug=True)

db.create_all()

if not User.query.filter_by(username='admin').first():
    admin = User(username='admin', password='admin')
    db.session.add(admin)
    db.session.commit()
