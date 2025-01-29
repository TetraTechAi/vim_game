from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # データベース設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vim_game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # データベースの初期化
    db.init_app(app)

    # モデルのインポート
    with app.app_context():
        from app.models import models

    # ルートの登録
    with app.app_context():
        from app.routes import game_routes, user_routes
        app.register_blueprint(game_routes.bp)
        app.register_blueprint(user_routes.bp)
        
        # データベースの作成
        db.create_all()

    return app
