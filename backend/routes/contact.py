import re
import requests
from flask import Blueprint, request, jsonify, current_app
from models import db, Submission

contact_bp = Blueprint('contact', __name__)

def verify_hcaptcha(token):
    secret = current_app.config['HCAPTCHA_SECRET_KEY']
    response = requests.post('https://hcaptcha.com/siteverify', data={
        'secret': secret,
        'response': token
    })
    result = response.json()
    return result.get('success', False)

@contact_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()

    # hCaptcha verification
    hcaptcha_token = data.get('hcaptcha_token', '')
    if not verify_hcaptcha(hcaptcha_token):
        return jsonify({'success': False, 'message': 'CAPTCHA verification failed. Please try again.'}), 400

    # Field validation
    name = data.get('name', '').strip()
    country_code = data.get('country_code', '+91').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not all([name, country_code, phone, email, message]):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    # Phone validation — digits only, 5 to 15 digits
    if not re.match(r'^\d{5,15}$', phone):
        return jsonify({'success': False, 'message': 'Please enter a valid phone number.'}), 400

    # Email validation
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
