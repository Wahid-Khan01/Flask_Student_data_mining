from functools import wraps
from flask import request, jsonify
import jwt
from core import secret_key

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error':'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1] if token.startswith('Bearer ') else token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload['id']

        except jwt.ExpiredSignatureError:
            return jsonify({'message':'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message':'Invalid token'}), 401
        
        return func(*args, **kwargs)
    
    return decorated_function