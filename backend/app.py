from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vim_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ルートのインポート
from app.routes import game_routes, user_routes

# ルートの登録
app.register_blueprint(game_routes.bp)
app.register_blueprint(user_routes.bp)

if __name__ == '__main__':
    # データベースの作成
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
