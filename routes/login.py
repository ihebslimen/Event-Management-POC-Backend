# routes.py
from flask import Blueprint, jsonify, request, abort
from werkzeug.security import  check_password_hash, generate_password_hash
from models.users import User
from utils.db import db
from flask_cors import CORS
import jwt
import datetime
from jwt.api_jwt import encode
import os
from datetime import datetime , timedelta, timezone


SECRET_KEY =  os.environ.get('SECRET_KEY')



login_bp = Blueprint('login',__name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    print(generate_password_hash(data['password'], method='pbkdf2:sha256'))
    if user and  check_password_hash(user.password_hash,password):
        payload = {}
        # Create access token (e.g. using JWT)
        user_id = user.id
        role= user.role
        payload = {'user_id': user_id, 'role' : role, 'exp': datetime(9999, 12, 31)}
        access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        res = jsonify({"Message" :"Login successfully" , "data": access_token, "user_id": user_id })
        res.status_code = 200
        return res
    res = jsonify({"Error" : 'Wrong Credentials'})
    res.status_code = 400
    return res



CORS(login_bp, origins='*', allow_headers=["Content-Type"])

@login_bp.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = login_bp.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        return response
    



