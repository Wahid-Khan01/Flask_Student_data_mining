from flask import Blueprint, jsonify, request, make_response, session
from marshmallow import ValidationError
from hashlib import sha256
import jwt
from core.dbs.models import User
from core.dbs.serde import users_schema
from datetime import datetime, timezone, timedelta
from core import secret_key

login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
def post():
    data = request.json
    if not data:
        return jsonify({'message': 'No JSON data provided'}), 400
    try:
        login_data = {'email': data.get('email'), 'password': data.get('password')}
        validated_data = users_schema(only=('email', 'password')).load(login_data)
    except ValidationError as e:
        return jsonify({'message':'Validation error', 'errors': e.messages})
    user = User.query.filter_by(email=validated_data.get('email')).first()
    hashed_password = sha256(validated_data['password'].encode('utf-8')).hexdigest()
    if user and user.password == hashed_password:
        session['id'] = user.id
        expiry = datetime.now(timezone.utc) + timedelta(minutes=60)
        payload = {'id':user.id, 'email':validated_data['email'],'expiry':expiry.timestamp()}
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        response = make_response(jsonify({'message':'Login Succesful', 'token': token}))
        response.set_cookie('token', token, httponly=True)
        return response
    else:
        return jsonify({'message':'Invalid Credentials'}), 401
