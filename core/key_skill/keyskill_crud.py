from flask import Blueprint, request, jsonify
from core import db
from core.dbs.models import UserSkill
from core.token_func.token_function import token_required
from core.token_func.get_token import get_user_id_from_token


user_skill_bp = Blueprint('user_skill_bp', __name__)

# Add a key skill for the logged-in user
@user_skill_bp.route('/user_skill_add', methods=['POST'])
@token_required
def add_user_skill():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ', '')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    skill = request.json.get('skills')
    if not skill:
        return jsonify({'message': 'Skill is required'}), 400

    user_skill = UserSkill.query.filter_by(user_id=user_id).first()
    if user_skill:
        user_skill.skills += f",{skill}"
    else:
        user_skill = UserSkill(user_id=user_id, skills=skill)
        db.session.add(user_skill)

    db.session.commit()
    
    return jsonify({'message': 'Key skill added successfully'}), 201

# Get all key skills of the logged-in user
@user_skill_bp.route('/user_skill_view', methods=['GET'])
@token_required
def get_user_skills():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    user_skill = UserSkill.query.filter_by(user_id=user_id).first()
    if not user_skill:
        return jsonify({'message': 'No key skills found for the user'}), 404

    skills = user_skill.skills.split(',')
    return jsonify({'skills': skills}), 200

# Delete a key skill of the logged-in user
@user_skill_bp.route('/user_skill_del/<string:skill>', methods=['DELETE'])
@token_required
def delete_user_skill(skill):
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ','')
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'User ID not found in token'}), 401

    user_skill = UserSkill.query.filter_by(user_id=user_id).first()
    if not user_skill:
        return jsonify({'message': 'No key skills found for the user'}), 404

    skills = user_skill.skills.split(',')
    if skill not in skills:
        return jsonify({'message': 'Key skill not found for the user'}), 404

    skills.remove(skill)
    user_skill.skills = ','.join(skills)
    db.session.commit()

    return jsonify({'message': 'Key skill deleted successfully'}), 200
