import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.Blog import Blog, BlogCeate, BlogList, Blogs
from resources.User import SignUp, SignIn

app = Flask(__name__)
CORS(app)
uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mithun'
api = Api(app)

api.add_resource(SignUp, '/api/auth/signup')
api.add_resource(SignIn, '/api/auth/login')

api.add_resource(BlogCeate, '/api/blogs/create')
api.add_resource(Blog, '/api/blogs/blog/<string:blogid>')
api.add_resource(BlogList, '/api/blogs/blogList')
api.add_resource(Blogs, '/api/blogs/myBlog/<string:username>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)