from flask import Blueprint, request, jsonify
from core import db
from core.dbs.models import ResumeHeadline
from core.token_func.token_function import token_required
from core.token_func.get_token import get_user_id_from_token



resume_headline_bp = Blueprint('resume_headline', __name__)

# Create or update the resume headline for the logged-in user
@resume_headline_bp.route('/resume_headline_add', methods=['POST', 'PUT'])
@token_required
def manage_resume_headline():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    data = request.get_json()
    headline_text = data.get('headline')

    # Check if the user already has a resume headline
    existing_headline = ResumeHeadline.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        # If the user doesn't have a headline, create a new one
        if not existing_headline:
            new_headline = ResumeHeadline(user_id=user_id, headline=headline_text)
            db.session.add(new_headline)
            db.session.commit()
            return jsonify({'message': 'Resume headline created successfully'}), 201
        else:
            return jsonify({'message': 'Resume headline already exists for the user'}), 400

    elif request.method == 'PUT':
        # If the user has an existing headline, update it
        if existing_headline:
            existing_headline.headline = headline_text
            db.session.commit()
            return jsonify({'message': 'Resume headline updated successfully'}), 200
        else:
            return jsonify({'message': 'No resume headline found for the user'}), 404

# Get the resume headline for the logged-in user
@resume_headline_bp.route('/resume_headline_view', methods=['GET'])
@token_required
def get_resume_headline():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    # Retrieve the resume headline for the user
    headline = ResumeHeadline.query.filter_by(user_id=user_id).first()

    if headline:
        return jsonify({'headline': headline.headline}), 200
    else:
        return jsonify({'message': 'No resume headline found for the user'}), 404

# Delete the resume headline for the logged-in user
@resume_headline_bp.route('/resume_headline_del', methods=['DELETE'])
@token_required
def delete_resume_headline():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    # Retrieve and delete the resume headline for the user
    headline = ResumeHeadline.query.filter_by(user_id=user_id).first()

    if headline:
        db.session.delete(headline)
        db.session.commit()
        return jsonify({'message': 'Resume headline deleted successfully'}), 200
    else:
        return jsonify({'message': 'No resume headline found for the user'}), 404
