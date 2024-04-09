from flask import request, Blueprint, jsonify, send_file
from core.dbs.models import PDFModel
from core import db
import io
from core.token_func.token_function import token_required
import jwt
from core import secret_key
from core.token_func.get_token import get_user_id_from_token

pdf_upload = Blueprint('pdf_upload', __name__)


@pdf_upload.route('/upload', methods=['POST'])
@token_required
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'message':'No data provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'No selected file'})
    
    file_data = file.read()

    token = request.headers.get('Authorization') 
    token = token.replace('Bearer ','') # Example: 'Bearer <token>'
    # print(token)
    # Extract user ID from the token
    user_id = get_user_id_from_token(token) # Implement this function to extract user ID from the token
    # print(user_id)
    existing_file = PDFModel.query.filter_by(user_id=user_id).first()
    if existing_file:
        db.session.delete(existing_file)
        db.session.commit()

    pdf_model = PDFModel(data=file_data, user_id=user_id)  # Set the user ID
    db.session.add(pdf_model)
    db.session.commit()

    return jsonify({'message':'File uploaded successfully'})

@pdf_upload.route('/delete', methods=['DELETE'])
@token_required
def delete():
    pdf_model = PDFModel.query.first()
    if not pdf_model:
        return jsonify({'message':'No file found'})
    db.session.delete(pdf_model)
    db.session.commit()
    return jsonify({'message':'File deleted successfully'})


@pdf_upload.route('/download', methods=['GET'])
@token_required
def get():
    pdf_model = PDFModel.query.first()
    if not pdf_model:
        return jsonify({'message':'No files available'})
    pdf_data = pdf_model.data

    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf', #multipurpose internet mail extensions
        as_attachment=True,
        download_name='downloaded_pdf.pdf'
    )