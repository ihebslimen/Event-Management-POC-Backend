from functools import wraps
from flask import  jsonify, request, abort
from models.users import User
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime,timezone
from utils.db import db



load_dotenv()

SECRET_KEY =  os.environ.get('SECRET_KEY')

def loggedin():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                res = jsonify({"Error" : " Authorization Header Missing"})
                res.status_code = 400
                abort(res)
            jwt_token = auth_header.split(' ')[1]
            try:
                decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                ##print(decoded_token)
            except jwt.ExpiredSignatureError:
                res = jsonify({"Error" : "Accès non autorisée"})
                res.status_code = 401
                abort(res)
            except jwt.InvalidTokenError:
                res = jsonify({"Error" : "Accès non autorisée"})
                res.status_code = 401
                abort(res)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                res = jsonify({"Error" : " Authorization Header Missing"})
                res.status_code = 400
                abort(res)
            jwt_token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            #print(decoded_token)
            if decoded_token['role'] != required_role:
                res = jsonify({"Error" : "Accès non autorisée"})
                res.status_code = 401
                abort(res)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def id_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                res = jsonify({"Error" : " Authorization Header Missing"})
                res.status_code = 400
                abort(res)
            jwt_token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            #print(decoded_token)
            if decoded_token['user_id'] != user_id:
                res = jsonify({"Error" : "Accès non autorisée"})
                res.status_code = 401
                abort(res)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def user_management():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')

            auth_header = request.headers.get('Authorization')
            if not auth_header:
                res = jsonify({"Error" : " Authorization Header Missing"})
                res.status_code = 400
                abort(res)
            jwt_token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            #print(decoded_token)
            if decoded_token["role"] != "admin" and user_id != decoded_token['user_id']:
                res = jsonify({"Error" : "Accès non autorisée"})
                res.status_code = 401
                abort(res)
            return func(*args, **kwargs)
        return wrapper
    return decorator













def check_expiration():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                res = jsonify({"Error" : " Authorization Header Missing"})
                res.status_code = 400
                abort(res)
            jwt_token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token['user_id']
            #print(user_id)
            user = User.query.filter_by(id=user_id).first()
            user_dict  = user.to_dict()
            #print(user_dict)
            if user.role == "user" and (user.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) or user.is_active == False):
                user.is_active = False
                db.session.commit()
                res = jsonify({"Error" : "Utilisateur expiré"})
                res.status_code = 403
                abort(res)
            return func(*args, **kwargs)
        return wrapper
    return decorator