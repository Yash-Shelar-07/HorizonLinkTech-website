import csv
import io
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, current_app, Response
from models import db, Submission, Note

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if (username == current_app.config['ADMIN_USERNAME'] and
                password == current_app.config['ADMIN_PASSWORD']):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        error = 'Invalid username or password.'
    return render_template('admin/login.html', error=error)

@admin_bp.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '').strip()

    query = Submission.query

    if status_filter:
        query = query.filter(Submission.status == status_filter)

    if search:
        like = f'%{search}%'
        query = query.filter(
            db.or_(
                Submission.name.ilike(like),
                Submission.email.ilike(like),
                Submission.phone.ilike(like)
            )
        )

    submissions = query.order_by(Submission.created_at.desc()).all()
    statuses = ['New', 'Contacted', 'In Progress', 'Closed']
    return render_template('admin/dashboard.html',
                           submissions=submissions,
                           statuses=statuses,
                           status_filter=status_filter,
                           search=search)

@admin_bp.route('/admin/submission/<int:submission_id>')
@login_required
def detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    statuses = ['New', 'Contacted', 'In Progress', 'Closed']
    return render_template('admin/detail.html', submission=submission, statuses=statuses)

@admin_bp.route('/admin/submission/<int:submission_id>/status', methods=['POST'])
@login_required
def update_status(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    new_status = request.form.get('status')
    statuses = ['New', 'Contacted', 'In Progress', 'Closed']
    if new_status in statuses:
        submission.status = new_status
        db.session.commit()
    return redirect(url_for('admin.detail', submission_id=submission_id))

@admin_bp.route('/admin/submission/<int:submission_id>/note', methods=['POST'])
@login_required
def add_note(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    content = request.form.get('content', '').strip()
    if content:
        note = Note(submission_id=submission.id, content=content)
        db.session.add(note)
        db.session.commit()
    return redirect(url_for('admin.detail', submission_id=submission_id))

@admin_bp.route('/admin/submission/<int:submission_id>/delete', methods=['POST'])
@login_required
def delete_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/export')
@login_required
def export_csv():
    submissions = Submission.query.order_by(Submission.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Country Code', 'Phone', 'Email', 'Message', 'Status', 'Submitted At'])
    for s in submissions:
        writer.writerow([s.id, s.name, s.country_code, s.phone, s.email, s.message, s.status, s.created_at.strftime('%Y-%m-%d %H:%M')])
    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=submissions.csv'})
