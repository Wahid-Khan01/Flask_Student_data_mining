from flask import Blueprint, jsonify, request
from core import db
from core.dbs.models import Education
from core.dbs.serde import education_schema
from core.token_func.get_token import get_user_id_from_token
from core.token_func.token_function import token_required

education_bp = Blueprint('education', __name__)

@education_bp.route('/education_add', methods=['POST'])
@token_required
def add_education():
    data = request.get_json()
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    data['user_id'] = user_id
    education = education_schema().load(data)
    db.session.add(education)
    db.session.commit()
    return education_schema.jsonify(education), 201

@education_bp.route('/education_view', methods=['GET'])
@token_required
def get_educations():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    educations = Education.query.filter_by(user_id=user_id).all()
    return education_schema.jsonify(educations), 200

@education_bp.route('/education_update', methods=['PUT'])
@token_required
def update_education():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    data = request.get_json()
    education_id = data.get('id')
    if education_id is None:
        return jsonify({'error': 'Education ID is missing'}), 400
    
    education = Education.query.filter_by(id=education_id, user_id=user_id).first()
    if education is None:
        return jsonify({'error': 'Education entry not found'}), 404
    
    # Update the education entry
    education = education_schema.load(data, instance=education, partial=True)
    db.session.commit()
    return education_schema.jsonify(education), 200


@education_bp.route('/education_delete', methods=['DELETE'])
@token_required
def delete_education():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    data = request.get_json()
    education_id = data.get('id')
    if education_id is None:
        return jsonify({'error': 'Education ID is missing'}), 400
    
    education = Education.query.filter_by(id=education_id, user_id=user_id).first()
    if education is None:
        return jsonify({'error': 'Education entry not found'}), 404
    
    # Delete the education entry
    db.session.delete(education)
    db.session.commit()
    return jsonify({'message': 'Education entry deleted successfully'}), 200