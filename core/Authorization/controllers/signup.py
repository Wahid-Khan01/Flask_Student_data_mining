from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from hashlib import sha256
from core.dbs.models import User
from core.dbs.serde import users_schema
from core import db

signup = Blueprint('signup', __name__)
@signup.route('/signup', methods=['POST'])
def post():
    data = request.json

    if not data:
        return jsonify({'message':'No data Provided'}), 400

    try:
        validated_data = users_schema().load(data)

    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors':e.messages}), 400

    if User.query.filter_by(email=validated_data['email']).count():
        return jsonify({'message':'Email already registered Kindly login to continue'}), 409

    if len(validated_data['full_name']) < 3:
        return({'message':'Username Should have more than 2 Characters'})
    
    if len(validated_data['password']) < 8:
        return ({'message':'Password must be atleast 8 chracters long'})
    
    hashed_password = sha256(data['password'].encode('utf-8')).hexdigest()
    
    new_user = User(
        full_name=validated_data['full_name'],
        email=validated_data['email'],
        password=hashed_password,
        mobile_number=validated_data['mobile_number'],
        is_fresher=validated_data['is_fresher'],
        allow_updates=validated_data['allow_updates']
    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'An error Occured while processing your request'}), 500
    
    return jsonify({'message':'Signed Up Successfully'}), 200