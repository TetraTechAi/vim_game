from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # データベースの設定
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vim_game.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CORSの設定
    CORS(app)
    
    # データベースの初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
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
