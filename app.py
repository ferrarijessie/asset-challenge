from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Additional configuration based on environment
app.config['TESTING'] = os.getenv('FLASK_ENV') == 'testing'
app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'

db = SQLAlchemy(app)

# Static API key
API_KEY = 'Dyn4m1cAsS3tKey'

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return {'message': 'Unauthorized'}, 401
    return decorated
migrate = Migrate(app, db)

# Import routes after db initialization to avoid circular imports
from api import api
api.init_app(app)

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
