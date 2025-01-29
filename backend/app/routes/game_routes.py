from flask import Blueprint, jsonify, request
from app.models.models import VimCommand, WeakPoint, Progress
from app import db
import random

bp = Blueprint('game', __name__, url_prefix='/api/game')

@bp.route('/commands/<int:level>', methods=['GET'])
def get_commands(level):
    """指定されたレベルのコマンドを取得"""
    commands = VimCommand.query.filter_by(difficulty_level=level).all()
    return jsonify([{
        'id': c.id,
        'command': c.command,
        'description': c.description,
        'category': c.category
    } for c in commands])

@bp.route('/weak-points/<int:user_id>', methods=['GET'])
def get_weak_points(user_id):
    """ユーザーの苦手なコマンドを取得"""
    weak_points = WeakPoint.query.filter_by(user_id=user_id)\
        .order_by(WeakPoint.mistake_count.desc())\
        .limit(10)\
        .all()
    return jsonify([{
        'command': w.command,
        'mistake_count': w.mistake_count,
        'difficulty_level': w.difficulty_level
    } for w in weak_points])

@bp.route('/weak-points', methods=['POST'])
def add_weak_point():
    """苦手なコマンドを記録"""
    data = request.get_json()
    weak_point = WeakPoint.query.filter_by(
        user_id=data['user_id'],
        command=data['command'],
        difficulty_level=data['difficulty_level']
    ).first()

    if weak_point:
        weak_point.mistake_count += 1
    else:
        weak_point = WeakPoint(
            user_id=data['user_id'],
            command=data['command'],
            difficulty_level=data['difficulty_level'],
            mistake_count=1
        )
        db.session.add(weak_point)

    db.session.commit()
    return jsonify({'message': '苦手なコマンドを記録しました'})

@bp.route('/progress', methods=['POST'])
def save_progress():
    """ゲームの進捗を保存"""
    data = request.get_json()
    progress = Progress(
        user_id=data['user_id'],
        level=data['level'],
        score=data['score']
    )
    db.session.add(progress)
    db.session.commit()
    return jsonify({'message': '進捗が保存されました'})

@bp.route('/generate-question/<int:user_id>/<int:level>', methods=['GET'])
def generate_question(user_id, level):
    """問題を生成"""
    # 苦手なコマンドを優先的に出題（70%の確率）
    if random.random() < 0.7:
        weak_points = WeakPoint.query.filter_by(
            user_id=user_id,
            difficulty_level=level
        ).order_by(WeakPoint.mistake_count.desc()).limit(5).all()
        
        if weak_points:
            command = random.choice(weak_points)
            return jsonify({
                'command': command.command,
                'difficulty_level': command.difficulty_level
            })
    
    # ランダムなコマンドを出題
    commands = VimCommand.query.filter_by(difficulty_level=level).all()
    if commands:
        command = random.choice(commands)
        return jsonify({
            'command': command.command,
            'description': command.description,
            'difficulty_level': command.difficulty_level
        })
    
    return jsonify({'error': '問題の生成に失敗しました'}), 404
