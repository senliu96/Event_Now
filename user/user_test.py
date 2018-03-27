from flask import Flask
from flask_mongoengine import MongoEngine
import unittest
from user.models import User

db = MongoEngine()
app = Flask(__name__)
app.config['MONGODB_DB'] = 'eventnow'
app.config['MONGODB_HOST'] = 'ds259865.mlab.com'
app.config['MONGODB_PORT'] = 59865
app.config['MONGODB_USERNAME'] = 'eventnowAdmin'
app.config['MONGODB_PASSWORD'] = 'eventnow'
db.init_app(app)
User.objects.filter(name="Tom").delete()
tclass = User(db.Document)


class Testusercount(unittest.TestCase):
    def test_count1(self):
        self.assertEqual(tclass.countuser("Tom"), 0)

    def test_count2(self):
        test_user1 = User(
            name="Tom",
            email="tom2@gmail.com",
            password="tom123"
        )
        test_user1.save()
        self.assertEqual(tclass.countuser("Tom"), 1)

    def test_count3(self):
        test_user2 = User(
            name="Tom",
            email="tom3@gmail.com",
            password="tom123"
        )
        test_user2.save()
        self.assertEqual(tclass.countuser("Tom"), 2)




unittest.main()
print(User.objects.filter(name="Tom").count())
