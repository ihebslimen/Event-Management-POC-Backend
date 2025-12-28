from flask import Blueprint, jsonify, request, abort
from werkzeug.security import generate_password_hash
from models.users import User
from utils.db import db
from flask_cors import CORS
from utils.decorators import role_required, loggedin, user_management
from datetime import datetime, timedelta,timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY =  os.environ.get('SECRET_KEY')

users_bp = Blueprint('users', __name__)

# Route to get all users
@users_bp.route('/', methods=['GET'])
@role_required('admin')
def get_all_users():
    try:
        # Get all users
        users = User.query.all()
  
        # Convert users to an array of dictionaries
        users_list = [user.to_dict() for user in users]
        response = jsonify(users=users_list)
        response.status_code = 200

        return response
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    
    finally:
        db.session.close()


# Route to get a specific user by ID
@users_bp.route('/<int:user_id>', methods=['GET'])
@user_management()
def get_user(user_id):
    try:
        # Get a specific user by ID
        user = User.query.get(user_id)

        if user is None:
            return jsonify(message='Utilisateur non trouvé'), 404

        # Convert the user to a dictionary
        user_dict = user.to_dict()

        response = jsonify(user=user_dict)
        response.status_code = 200

        return response
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    
    finally:
        db.session.close()


# Route to create a new user
@users_bp.route('/', methods=['POST'])
@role_required('admin')
def create_user():
    try:
        # Get user data from the request
        data = request.get_json()
        valid_columns = {col.name for col in User.__table__.columns}
        sent_keys = set(data.keys())
        sent_keys.remove("password")
        sent_keys.add("password_hash")
        invalid_keys = sent_keys - valid_columns
        if invalid_keys:
            abort(400, description=f"Champs invalides: {', '.join(invalid_keys)}")

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Create a new user
        new_user = User(
            username=data['username'],
            password_hash=hashed_password, 
            role = data["role"])
        # Add the user to the session and commit the changes
        db.session.add(new_user)
        db.session.commit()

        response = jsonify(message='Utilisateur ajouté avec success')
        response.status_code = 200

        return response
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    
    finally:
        db.session.close()


# Route to update an existing user by ID
@users_bp.route('/<int:user_id>', methods=['PUT'])
@user_management()
def update_user(user_id):
    try:

        data = request.get_json()
        # Get the existing user by ID
        # Get user data from the request
        valid_columns = {col.name for col in User.__table__.columns}
        sent_keys = set(data.keys())
        sent_keys.remove("password")
        sent_keys.add("password_hash")
        invalid_keys = sent_keys - valid_columns
        if invalid_keys:
            abort(400, description=f"Champs invalides: {', '.join(invalid_keys)}")
        user = User.query.get(user_id)

        if user is None:
            return jsonify(message='Utilisateur non trouvé'), 404

        # Update user information
        if "username" in data:
            user.username = data['username']
       
        if "password" in data:
            user.password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')
        if "role" in data:
            user.role = data["role"]
        # Commit the changes
        db.session.commit()

        response = jsonify(message='Utilisateur mis à jour avec success')
        response.status_code = 200

        return response
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    
    finally:
        db.session.close()


# Route to delete an existing user by ID
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required("admin")
def delete_user(user_id):
    try:
        # Get the existing user by ID
        user = User.query.get(user_id)

        if user is None:
            return jsonify(message='Utilisateur non trouvé'), 404

        # Delete the user from the session and commit the changes
        db.session.delete(user)
        db.session.commit()

        response = jsonify(message='Utilisateur supprimé avec success')
        response.status_code = 200

        return response
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    
    finally:
        db.session.close()
    



CORS(users_bp, origins='*', allow_headers=["Content-Type"])

@users_bp.before_request
@loggedin()
def handle_preflight():
    if request.method == 'OPTIONS':
        response = users_bp.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        return response