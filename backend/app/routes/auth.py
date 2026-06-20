import logging
import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import get_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')
logger = logging.getLogger(__name__)


@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        
        # Check if user exists
        if db.users.find_one({'email': email}):
            return jsonify({'error': 'User already exists'}), 409
        
        # Hash password and save user
        hashed = generate_password_hash(password)
        user = {
            'email': email,
            'password': hashed,
            'createdAt': datetime.utcnow(),
            'isActive': True
        }
        db.users.insert_one(user)
        
        logger.info(f'New user registered: {email}')
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        logger.exception('Failed to register user')
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        user = db.users.find_one({'email': email})
        
        if not user or not check_password_hash(user['password'], password):
            logger.warning(f'Failed login attempt for: {email}')
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.get('isActive', True):
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Generate JWT token
        token = jwt.encode(
            {
                'email': email,
                'userId': str(user.get('_id', '')),
                'exp': datetime.utcnow() + timedelta(days=7)
            },
            os.getenv('SECRET_KEY', 'change-me-in-production'),
            algorithm='HS256'
        )
        
        logger.info(f'User logged in: {email}')
        return jsonify({
            'token': token,
            'email': email,
            'userId': str(user.get('_id', ''))
        }), 200
        
    except Exception as e:
        logger.exception('Failed to authenticate user')
        return jsonify({'error': 'Authentication failed'}), 500


@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user():
    """Get current user info from JWT token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        decoded = jwt.decode(
            token,
            os.getenv('SECRET_KEY', 'change-me-in-production'),
            algorithms=['HS256']
        )
        
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        user = db.users.find_one({'email': decoded['email']}, {'password': 0})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'email': user['email'],
            'userId': str(user.get('_id', '')),
            'createdAt': user['createdAt'],
            'isActive': user.get('isActive', True)
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        logger.exception('Failed to get current user')
        return jsonify({'error': 'Failed to get user info'}), 500


def require_auth(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            decoded = jwt.decode(
                token,
                os.getenv('SECRET_KEY', 'change-me-in-production'),
                algorithms=['HS256']
            )
            request.user = decoded
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated
