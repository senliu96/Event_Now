from application import db
import datetime


class User(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now)
    bio = db.StringField(max_length = 200)
    profile_image =db.StringField()
    def countuser(self,username):
            num = User.objects.filter(name=username).count()
            return num
