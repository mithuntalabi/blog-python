from flask import request
from flask_restful import Resource
from sqlalchemy.sql import func
import jwt
import bcrypt
from models.User import UserModel
from datetime import datetime, timedelta

SECRETE = "mithunsecretekey"

class SignUp(Resource):
    def post(self):
        body = request.get_json();
        username = body.get("username")

        user = UserModel.find_by_username(username)
        if user != None:
            return {"success": True, "error": "USERNAME_EXISTS"}, 409

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(body.get("password").encode(), salt)

        userData = UserModel(username, hashedPassword)
        try:
            userData.save_to_db()
        except:
            return {"success": False, "message": "Database connection errror"}, 500
        dt = datetime.utcnow() + timedelta(hours=9)
        token = jwt.encode({"userId": userData.id, "username": username, "exp": dt}, SECRETE, algorithm="HS256")
        decodedResult = _getToken_Data(token)
        return decodedResult, 200

class SignIn(Resource):
    def post(self):
        body = request.get_json();
        username = body.get("username")

        user = UserModel.find_by_username(username)
        if user == None:
            return {"success": False, "error": "USERNAME_NOT_FOUND"}, 409
        print(user.password.encode())
        if bcrypt.checkpw(body.get("password").encode(), user.password.encode()):
            dt = datetime.utcnow() + timedelta(hours=9)
            token = jwt.encode({"exp": dt, "userId": user.id, "username": username }, SECRETE)
            decodedResult = _getToken_Data(token)
            return decodedResult, 200
        return {"success": False, "error": "INVALID_PASSWORD"}, 403

def _getToken_Data(token):
    decodedData = jwt.decode(token, SECRETE, algorithms=["HS256"])
    return {'userId': decodedData.get('userId'), 'username': decodedData.get('username'), 'token': token, 'expiresIn': decodedData.get('exp')}