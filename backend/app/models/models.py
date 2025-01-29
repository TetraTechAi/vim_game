from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    progress = db.relationship('Progress', backref='user', lazy=True)
    weak_points = db.relationship('WeakPoint', backref='user', lazy=True)

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeakPoint(db.Model):
    __tablename__ = 'weak_points'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    command = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VimCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
