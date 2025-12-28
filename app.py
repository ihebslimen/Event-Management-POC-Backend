from flask import Flask, request
from dotenv import load_dotenv
from urllib.parse import quote
from utils.db import db
from flask_cors import CORS
from utils.decorators import *
import os

load_dotenv()
app = Flask(__name__)


user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database = os.environ.get('MYSQL_DATABASE')
secret_key =  os.environ.get('SECRET_KEY')
encoded_password = quote(password, safe='')

DATABASE_CONNECTION_URI = f'mysql://{user}:{encoded_password}@{host}/{database}'
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = secret_key
#### JWT Configuration
app.config['JWT_TOKEN_LOCATION'] = "headers"
app.config['JWT_HEADER_NAME'] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_IDENTITY_CLAIM"] = "user_id"    
# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)

# Add this to app.py after db.init_app(app)
with app.app_context():
    db.create_all()

from routes.users import users_bp
from routes.login import login_bp
from routes.event import event_bp

CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
CORS(users_bp, origins='*', allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],   supports_credentials = True)
CORS(event_bp, origins='*', allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],   supports_credentials = True)
CORS(app, origins='*', allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],   supports_credentials = True)


app.register_blueprint(event_bp, url_prefix = '/event')
app.register_blueprint(users_bp, url_prefix='/users')


app.register_blueprint(login_bp, url_prefic = '/')


CORS(app, origins='*', allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],   supports_credentials = True)



@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Access-Control-Allow-Credentials')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



