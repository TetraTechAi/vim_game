from flask import Blueprint, jsonify, request, current_app
from app.models.models import VimCommand, WeakPoint, Progress
from app import db
import random
from collections import defaultdict, deque
import logging
import jwt

# ロガーの設定
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('game', __name__, url_prefix='/api/game')

# 最後に出題されたコマンドを記録する辞書（過去3回分）
command_history = defaultdict(lambda: {'recent': deque(maxlen=3), 'last': None})

def get_user_id_from_token():
    """トークンからユーザーIDを取得"""
    token = request.headers.get('Authorization')
    if not token:
        return None
    
    try:
        token = token.split(' ')[1]  # "Bearer "を除去
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@bp.route('/debug/commands/<int:level>', methods=['GET'])
def debug_commands(level):
    """デバッグ用：指定されたレベルの全コマンドを取得"""
    commands = VimCommand.query.filter_by(difficulty_level=level).all()
    return jsonify([{
        'id': c.id,
        'command': c.command,
        'description': c.description,
        'category': c.category
    } for c in commands])

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
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': '認証が必要です'}), 401
    
    data = request.get_json()
    if not all(k in data for k in ['command', 'difficulty_level']):
        return jsonify({'error': '必須フィールドが不足しています'}), 400
    
    weak_point = WeakPoint.query.filter_by(
        user_id=user_id,
        command=data['command'],
        difficulty_level=data['difficulty_level']
    ).first()

    if weak_point:
        weak_point.mistake_count += 1
    else:
        weak_point = WeakPoint(
            user_id=user_id,
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
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': '認証が必要です'}), 401
    
    data = request.get_json()
    if not all(k in data for k in ['level', 'score']):
        return jsonify({'error': '必須フィールドが不足しています'}), 400
    
    progress = Progress(
        user_id=user_id,
        level=data['level'],
        score=data['score']
    )
    db.session.add(progress)
    db.session.commit()
    
    return jsonify({'message': '進捗を保存しました'})

def get_command_str(command):
    """コマンドオブジェクトから文字列を取得"""
    if isinstance(command, str):
        return command
    elif isinstance(command, (VimCommand, WeakPoint)):
        return command.command
    return str(command)

def get_random_command(commands, user_id, level, is_weak_point=False):
    """過去3回と異なるコマンドをランダムに選択"""
    key = str(user_id)  # レベルに関係なく、ユーザーごとに履歴を管理
    history = command_history[key]
    recent_commands = history['recent']
    last_command = history['last']
    
    # デバッグ用のログ
    current_app.logger.debug(f"User {user_id}, Level {level}")
    current_app.logger.debug(f"Recent commands: {[get_command_str(cmd) for cmd in recent_commands]}")
    current_app.logger.debug(f"Last command: {get_command_str(last_command) if last_command else None}")
    current_app.logger.debug(f"Is weak point: {is_weak_point}")
    
    # コマンドの比較を修正
    available_commands = []
    recent_command_strs = {get_command_str(cmd) for cmd in recent_commands}
    last_command_str = get_command_str(last_command) if last_command else None
    
    for cmd in commands:
        cmd_str = get_command_str(cmd)
        if cmd_str not in recent_command_strs and cmd_str != last_command_str:
            available_commands.append(cmd)
    
    current_app.logger.debug(f"Available commands: {[get_command_str(cmd) for cmd in available_commands]}")
    
    if not available_commands:
        current_app.logger.debug("No available commands found, resetting history")
        recent_commands.clear()  # 履歴をクリア
        
        # 最後のコマンドを除外して利用可能なコマンドを取得
        if last_command_str:
            available_commands = [cmd for cmd in commands if get_command_str(cmd) != last_command_str]
        
        if not available_commands:
            current_app.logger.debug("No available commands even after reset, using all commands")
            available_commands = commands
    
    command = random.choice(available_commands)
    command_str = get_command_str(command)
    recent_commands.append(command_str)
    history['last'] = command_str
    
    current_app.logger.debug(f"Selected command: {command_str}")
    current_app.logger.debug(f"Updated recent commands: {[get_command_str(cmd) for cmd in recent_commands]}")
    return command

def get_available_levels(current_level):
    """出題可能なレベルのリストを取得"""
    levels = list(range(1, current_level + 1))
    weights = [0.3 if l < current_level else 0.7 for l in levels]
    return levels, weights

@bp.route('/generate-question/<int:level>', methods=['GET'])
def generate_question(level):
    """問題を生成（過去3回と異なる問題を出題）"""
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': '認証が必要です'}), 401
    
    current_app.logger.debug(f"Generating question for user {user_id}, level {level}")
    
    # 出題するレベルをランダムに選択（現在のレベル以下）
    available_levels, weights = get_available_levels(level)
    target_level = random.choices(available_levels, weights=weights, k=1)[0]
    
    current_app.logger.debug(f"Selected target level: {target_level}")
    
    # 苦手なコマンドを優先的に出題（70%の確率）
    if random.random() < 0.7:
        weak_points = WeakPoint.query.filter_by(
            user_id=user_id,
            difficulty_level=target_level
        ).order_by(WeakPoint.mistake_count.desc()).limit(5).all()
        
        current_app.logger.debug(f"Found {len(weak_points)} weak points")
        
        if weak_points:
            # 過去3回と異なる苦手コマンドを選択
            weak_point = get_random_command(weak_points, user_id, level, is_weak_point=True)
            if weak_point:
                command = VimCommand.query.filter_by(
                    command=weak_point.command,
                    difficulty_level=weak_point.difficulty_level
                ).first()
                
                if command:
                    current_app.logger.debug(f"Selected weak point command: {command.command}")
                    return jsonify({
                        'command': command.command,
                        'description': command.description,
                        'difficulty_level': command.difficulty_level
                    })
    
    # ランダムなコマンドを出題
    commands = VimCommand.query.filter_by(difficulty_level=target_level).all()
    current_app.logger.debug(f"Found {len(commands)} commands for level {target_level}")
    
    if commands:
        command = get_random_command(commands, user_id, level, is_weak_point=False)
        if command:
            current_app.logger.debug(f"Selected random command: {command.command}")
            return jsonify({
                'command': command.command,
                'description': command.description,
                'difficulty_level': command.difficulty_level
            })
    
    return jsonify({'error': '問題の生成に失敗しました'}), 404
