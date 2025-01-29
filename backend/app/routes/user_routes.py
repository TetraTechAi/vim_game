from flask import Blueprint, jsonify, request
from app.models.models import User, Progress
from app import db

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/register', methods=['POST'])
def register():
    """新規ユーザー登録"""
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'ユーザー名が既に使用されています'}), 400
    
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'id': user.id,
        'username': user.username
    })

@bp.route('/<int:user_id>/progress', methods=['GET'])
def get_progress(user_id):
    """ユーザーの進捗状況を取得"""
    progress = Progress.query.filter_by(user_id=user_id)\
        .order_by(Progress.completed_at.desc())\
        .all()
    return jsonify([{
        'level': p.level,
        'score': p.score,
        'completed_at': p.completed_at.isoformat()
    } for p in progress])

@bp.route('/<int:user_id>/stats', methods=['GET'])
def get_stats(user_id):
    """ユーザーの統計情報を取得"""
    user = User.query.get_or_404(user_id)
    progress = Progress.query.filter_by(user_id=user_id).all()
    
    total_score = sum(p.score for p in progress)
    max_level = max((p.level for p in progress), default=0)
    
    return jsonify({
        'username': user.username,
        'total_score': total_score,
        'max_level': max_level,
        'total_games': len(progress)
    })
