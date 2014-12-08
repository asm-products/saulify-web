from saulify import db
from saulify.models import User


db.create_all()

member = User(username='saul', email='saul@saulify.me')
member.hash_password('saul')
admin = User(username='admin', email='admin@saulify.me')
admin.role = 101
admin.hash_password('saul')

db.session.add(member)
db.session.add(admin)
db.session.commit()
