from flask import jsonify, session, Blueprint

logout = Blueprint('logout', __name__)

@logout.route('/logout', methods=['POST'])
def post():
    if 'id' not in session:
        return jsonify({'message': 'You need to login first'}), 401
    session.pop('id')
    return jsonify({'message': 'Successfully logged out'}), 200
