# # from application import create_app
# from flask import Flask
# from flask_mongoengine import MongoEngine
# from user.views import user_page
#
# db = MongoEngine()
# app = Flask(__name__)
# app.config['MONGODB_DB'] = 'eventnow'
# app.config['MONGODB_HOST'] = 'ds259865.mlab.com'
# app.config['MONGODB_PORT'] = 59865
# app.config['MONGODB_USERNAME'] = 'eventnowAdmin'
# app.config['MONGODB_PASSWORD'] = 'eventnow'
# app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = 'sl4263'
#
# db.init_app(app)
#
#
# @app.route("/")
# def hello():
#     return "Hello World!"
#
#
# app.register_blueprint(user_page, url_prefix="/user")
#
# app.run(host='127.0.0.1')
from application import create_app
app = create_app(config = 'config')
app.run(host='0.0.0.0')