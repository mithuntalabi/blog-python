from flask import request
from flask_restful import Resource
from sqlalchemy.sql import func
from models.Blog import BlogModel
import jwt

SECRETE = "mithunsecretekey"

class Blog(Resource):
    def patch(self, blogid):
        token = request.headers.get('Authorization')
        if token:
            isTokenValid = _verify_token(token)
            if not isTokenValid:
                return {"success": False, "error": "INVALID_TOKEN"}, 409
        else:
            return {"success": False, "error": "Access Denied! Unauthorized User"}, 409

        data = request.get_json();
        blog = BlogModel.find_by_blogid(blogid)
        if blog:
            blog.title = data.get("title")
            blog.content = data.get("content")
            try:
                blog.update_from_db()
            except:
                return {"success": True, "message": "Database connection errror"}, 500
        return {"message": "Updated blog successfully."}, 200

    def delete(self, blogid):
        token = request.headers.get('Authorization')
        if token:
            isTokenValid = _verify_token(token)
            if not isTokenValid:
                return {"success": False, "error": "INVALID_TOKEN"}, 409
        else:
            return {"success": False, "error": "Access Denied! Unauthorized User"}, 409

        blog = BlogModel.find_by_blogid(blogid)
        if blog:
            try:
                blog.delete_from_db()
            except:
                return {"success": True, "message": "Database connection errror"}, 500
        return {"message": "Deleted blog successfully."}, 200   

class BlogCeate(Resource):
    def post(self):
        token = request.headers.get('Authorization')
        if token:
            isTokenValid = _verify_token(token)
            if not isTokenValid:
                return {"success": False, "error": "INVALID_TOKEN"}, 409
        else:
            return {"success": False, "error": "Access Denied! Unauthorized User"}, 409

        data = request.get_json();
        blog = BlogModel(data.get("username"), data.get("title"), data.get("content"))
        try:
            blog.save_to_db()
        except:
            return {"success": True, "message": "Database connection errror"}, 500
        return {"success": True, "message": "Created blog successfully."}, 200

class Blogs(Resource):
    def get(self, username):
        token = request.headers.get('Authorization')
        if token:
            isTokenValid = _verify_token(token)
            if not isTokenValid:
                return {"success": False, "error": "INVALID_TOKEN"}, 409
        else:
            return {"success": False, "error": "Access Denied! Unauthorized User"}, 409
            
        return [blog.json() for blog in BlogModel.find_blog_by_username(username)]

class BlogList(Resource):
    def get(self):
        return [blog.json() for blog in BlogModel.query.all()]

def _verify_token(token):
    # bearer, _, tokenData = token.partition(' ')
    try:
        decode_token = jwt.decode(token, SECRETE, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
