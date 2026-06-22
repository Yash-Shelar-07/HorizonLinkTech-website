import re
from flask import Blueprint, request, jsonify
from models import db, Submission

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()

    name = data.get('name', '').strip()
    country_code = data.get('country_code', '+91').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not all([name, country_code, phone, email, message]):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    if not re.match(r'^\d{5,15}$', phone):
        return jsonify({'success': False, 'message': 'Please enter a valid phone number.'}), 400

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    try:
        submission = Submission(
            name=name,
            country_code=country_code,
            phone=phone,
            email=email,
            message=message
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Your requirement has been submitted successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Something went wrong. Please try again.'}), 500
