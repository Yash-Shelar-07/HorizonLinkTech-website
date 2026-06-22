from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(10), nullable=False, default='+91')
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='New')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='submission', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Submission {self.name} - {self.status}>'


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id} for Submission {self.submission_id}>'
