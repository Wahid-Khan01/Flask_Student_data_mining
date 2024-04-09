from flask import request, Blueprint, jsonify
from core.dbs.models import BasicDetailsFresher
from core import db
from core.token_func.token_function import token_required
from core.token_func.get_token import get_user_id_from_token
from core.dbs.serde import BasicDetailsFresher_schema



auth_blueprint = Blueprint('auth_blueprint', __name__)

# CREATE
@auth_blueprint.route('/add_detail', methods=['POST'])
@token_required
def add_basic_details():
    data = request.json
    token = request.headers.get('Authorization')
    token= token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)

    name = data['name']
    is_fresher = data['is_fresher']
    country_india = data['country_india']
    country_outside_india = data['country_outside_india']
    location = data['location']
    country_name = data.get('country_name', None) if not country_india else None

    basic_details = BasicDetailsFresher(name=name, is_fresher=is_fresher, 
                                        country_india=country_india, 
                                        country_outside_india=country_outside_india,
                                        location=location, country_name=country_name,
                                        phone=data['phone'], email=data['email'],
                                        availability=data['availability'], user_id=user_id)
    
    db.session.add(basic_details)
    db.session.commit()
    
    return jsonify({'message': 'Basic details added successfully'}), 201
# READ
@auth_blueprint.route('/fresher', methods=['GET'])
@token_required
def get_basic_details():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    basic_details = BasicDetailsFresher.query.filter_by(user_id=user_id).first()
    if basic_details:
        basic_details_schema = BasicDetailsFresher_schema()
        result = basic_details_schema.dump(basic_details)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Basic details not found'}), 404
    

@auth_blueprint.route('/update', methods=['PUT'])
@token_required
def update_basic_details():
    data = request.json
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)

    basic_details = BasicDetailsFresher.query.filter_by(user_id=user_id).first()
    if basic_details:
        basic_details.name = data.get('name', basic_details.name)
        basic_details.is_fresher = data.get('is_fresher', basic_details.is_fresher)
        basic_details.country_india = data.get('country_india', basic_details.country_india)
        basic_details.country_outside_india = data.get('country_outside_india', basic_details.country_outside_india)
        basic_details.location = data.get('location', basic_details.location)
        basic_details.country_name = data.get('country_name', basic_details.country_name)
        basic_details.phone = data.get('phone', basic_details.phone)
        basic_details.email = data.get('email', basic_details.email)
        basic_details.availability = data.get('availability', basic_details.availability)
        db.session.commit()
        return jsonify({'message': 'Basic details updated successfully'}), 200
    else:
        return jsonify({'error': 'Basic details not found'}), 404


# API endpoint to delete basic details by ID
@auth_blueprint.route('/delete', methods=['DELETE'])
@token_required
def delete_basic_details():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)

    basic_details = BasicDetailsFresher.query.filter_by(user_id=user_id).first()
    if basic_details:
        db.session.delete(basic_details)
        db.session.commit()
        return jsonify({'message': 'Basic details deleted successfully'}), 200
    else:
        return jsonify({'error': 'Basic details not found'}), 404


