from flask import Blueprint, jsonify, request
from app.models.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """ユーザー登録"""
    data = request.get_json()
    
    # 必須フィールドの確認
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': '必須フィールドが不足しています'}), 400
    
    # ユーザー名とメールアドレスの重複チェック
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'このユーザー名は既に使用されています'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'このメールアドレスは既に使用されています'}), 400
    
    # 新しいユーザーを作成
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'ユーザー登録が完了しました',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """ログイン"""
    data = request.get_json()
    
    # 必須フィールドの確認
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': '必須フィールドが不足しています'}), 400
    
    # ユーザーを検索
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'ユーザー名またはパスワードが正しくありません'}), 401
    
    # JWTトークンを生成
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, 'your-secret-key', algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@bp.route('/user', methods=['GET'])
def get_user():
    """現在のユーザー情報を取得"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '認証が必要です'}), 401
    
    try:
        token = token.split(' ')[1]  # "Bearer "を除去
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'ユーザーが見つかりません'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'トークンの有効期限が切れています'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '無効なトークンです'}), 401
